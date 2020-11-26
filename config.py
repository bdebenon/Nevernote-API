import os
from configparser import ConfigParser

from helpers.exceptions import ConfigMissingError


def is_file_in_curr_directory(filename):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if f.lower() == filename.lower():
            return True
    return False


def config(section):
    # Ensure we are in the proper directory
    config_file = "config.ini"
    levels_moved = 0
    while is_file_in_curr_directory(config_file) is False:
        os.chdir("..")
        levels_moved += 1
        if levels_moved > 10:
            raise ConfigMissingError(f"Unable to find {config_file}. 'config.ini' must be in the root directory.")

    filename = 'config.ini'
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgres
    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


if __name__ == "__main__":
    parameters = config("api_connection_settings")
    print(parameters)
