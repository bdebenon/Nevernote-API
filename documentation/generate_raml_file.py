# Confirmed to work with raml2html version 7.5.0

import os
import re
import subprocess


class ConfigMissingError(Exception):
    pass


def is_file_in_curr_directory(filename):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if f.lower() == filename.lower():
            return True
    return False


def get_root_directory():
    config_file = "config.ini"
    levels_moved = 0
    while is_file_in_curr_directory(config_file) is False:
        os.chdir("..")
        levels_moved += 1
        if levels_moved > 10:
            raise ConfigMissingError(f"Unable to find {config_file}. 'config.ini' must be in the root directory.")

    root_path = f"{os.getcwd()}/"
    return root_path


def get_lines_from_file(filepath):
    file = open(filepath, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


def process_route_line(line_text):
    try:
        regex_find_rule = r"(?<=rule=')(.*?)(?=')|(?<=rule=\")(.*?)(?=\")"
        detected_path_to_file = re.findall(regex_find_rule, line_text)[0][0]

        regex_find_all_methods = r"(?<=methods=\[)(.*?)(?=\])|(?<=methods=\[)(.*?)(?=\])"
        methods_string = re.findall(regex_find_all_methods, line_text)[0][0]
        methods_string = methods_string.lower()

        regex_find_specific_method = r"\"(.*?)\"|'(.*?)'"
        detected_methods = re.findall(regex_find_specific_method, methods_string)
        detected_methods = [x[0] for x in detected_methods]

        return detected_path_to_file, detected_methods
    except:
        return "/failure", ["GET"]


def parse_routes_from_file(file):
    # Flag variables
    ignore_next_route = False

    # Collect all routes to process
    collected_routes = []
    for index, line in enumerate(file):
        if "documentation_command:" in line:
            # Find the special commands and set appropriate flag variables
            command = line.split(":")[1]
            print(f"Special Command: {command}")
            if command == "ignore_next_route":
                ignore_next_route = True

        if "@app.route" in line:
            if ignore_next_route is True:
                ignore_next_route = False
                print(f"ignoring_route: {line}\n\n")
            else:
                path_to_file, methods = process_route_line(line)
                collected_routes.append({"path": path_to_file, "methods": methods})

    return collected_routes


def fetch_route_ramls(base_dir, routes):
    raml_lines = []
    for route in routes:
        path = route['path']
        partial_path = base_dir + "routes" + path + "/"
        methods = route['methods']
        for method in methods:
            route_raml_lines = ""
            route_raml_lines += f"{method}:\n"

            full_path = partial_path + method + ".py"
            f = open(full_path, "r")
            file_lines = f.readlines()

            collect_lines = False
            for line in file_lines:
                if "# RAML START #" in line:
                    collect_lines = True
                elif "# RAML END #" in line:
                    break
                elif collect_lines:
                    route_raml_lines += line
            raml_lines.append(route_raml_lines)

    return raml_lines


def fetch_route_structure(routes, ramls):
    structure = {}
    raml_index = 0
    for i in range(0, len(routes)):
        route = routes[i]
        for method in route["methods"]:
            raml = ramls[raml_index]
            path_list = route['path'].split('/')[1:]
            struct_dict = structure
            for j in range(0, len(path_list)):
                sub_path = path_list[j]
                if sub_path not in struct_dict:
                    struct_dict[sub_path] = {}
                struct_dict = struct_dict[sub_path]
                if j + 1 == len(path_list):
                    struct_dict[method] = raml
            raml_index += 1
    return structure


def get_current_version(root_dir):
    with open(root_dir + "version.txt") as f:
        version = f.readline()
    return version


def print_dict(output_file, d, indent=0):
    for k, v in d.items():
        if isinstance(v, dict):
            output_file.write(f"{indent * ' '}/{k}:\n")
            print_dict(output_file, v, indent + 4)
        else:
            lines_to_print = v.split("\n")
            for line in lines_to_print:
                output_file.write(f"{indent * ' '}{line}\n")


def write_raml_file(title, version, raml_structure_dict, output_directory):
    raml_file = open(f"{output_directory}/api_documentation.raml", "w")
    raml_file.write(f"#%RAML 1.0\n")
    raml_file.write("---\n")
    raml_file.write(f"title: {title}\n")
    raml_file.write(f"version: v{version}\n")
    print_dict(raml_file, raml_structure_dict)
    raml_file.close()


def convert_raml_to_html(output_directory, debug=False):
    try:
        raml_to_html_command = f"raml2html {output_directory}/api_documentation.raml > {output_directory}/api_documentation.html"
        if debug:
            file_null = open(os.devnull, 'w')
            subprocess.check_call(str(raml_to_html_command), shell=True, stdout=file_null, stderr=subprocess.STDOUT)
        else:
            subprocess.check_call(str(raml_to_html_command), shell=True)
    except subprocess.CalledProcessError:
        print("Failed to create html file from raml.")
        print("Please ensure you have raml2html version installed.")


if __name__ == "__main__":
    # Setup
    documentation_name = "Nevernote API - "

    # Collect info
    root_directory = get_root_directory()
    app_py_path = root_directory + "app.py"
    current_version = get_current_version(root_directory)
    _output_directory = f"{root_directory}/documentation/"

    # Main Flow
    app_py_lines = get_lines_from_file(app_py_path)
    parsed_routes = parse_routes_from_file(app_py_lines)
    route_ramls = fetch_route_ramls(root_directory, parsed_routes)
    route_structure = fetch_route_structure(parsed_routes, route_ramls)
    write_raml_file(documentation_name, current_version, route_structure, _output_directory)
    convert_raml_to_html(_output_directory)
