import json
import decimal


def load_file_from_json(path_to_json):
    try:
        with open(path_to_json) as json_file:
            user_json = json.load(json_file, parse_float=decimal.Decimal)
    except:
        user_json = "Error found. Need to in more error handling."
        print("load_user_from_json: Error found: Invalid JSON format identified.")
    return user_json
