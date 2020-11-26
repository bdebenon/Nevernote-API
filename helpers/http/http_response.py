import json
from enum import Enum


def http_failure_response(http_response_code, internal_response_code, message):
    response = {
        "error": {
            "internal_response_code": internal_response_code.value,
            "message": message,
            }
        }
    return json.dumps(response), http_response_code


def http_success_response(http_response_code, message):
    response = {"message": message}
    return json.dumps(response), http_response_code


class InternalResponseCode(Enum):
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    # 100 codes

    # 101 codes

    # 400 codes
    invalid_dict_parameters = 4001
    invalid_minimum_profile = 4002
    invalid_args_provided = 4003

    # 401 codes
    invalid_user_id_or_password = 4011

    # 404 codes
    basic_info_empty = 4041

    # 409 codes
    user_name_taken = 4091
    invalid_registration_code = 4092

    # 500 codes
    unknown_error = 5001
    database_error = 5002
    invalid_database_response = 5003

    # 503 codes
    database_did_not_respond = 5031
