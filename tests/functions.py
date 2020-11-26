import requests

from tests import get_api_endpoint, get_verify_ssl

api_endpoint = get_api_endpoint()
verify_ssl = get_verify_ssl()


# Note: You cannot send via params on POST. It comes into flask as data, not params
def send_post_request_with_json(__endpoint, __json):
    # Build HTTP Url
    url = f'{api_endpoint}{__endpoint}'

    # Create dict to be added to database
    args_json = __json

    # Sending get request and saving the response as response object
    response = requests.post(verify=verify_ssl, url=url, json=args_json)

    return response


def send_post_request_with_file(__endpoint, files, data):
    # Build HTTP Url
    url = f'{api_endpoint}{__endpoint}'

    # Sending get request and saving the response as response object
    # response = requests.post(url=url, data=files, json=json)
    response = requests.post(verify=verify_ssl, url=url, files=files, data=data)

    return response


def send_get_request_with_params_dict(__endpoint, __json):
    # Build HTTP Url
    url = f'{api_endpoint}{__endpoint}'

    # Create dict to be added to database
    args_json = __json

    # Sending get request and saving the response as response object
    response = requests.get(verify=verify_ssl, url=url, params=args_json)

    return response


def send_get_request_with_json(__endpoint, __json):
    # Build HTTP Url
    url = f'{api_endpoint}{__endpoint}'

    # Create dict to be added to database
    input_json = __json

    # Sending get request and saving the response as response object
    response = requests.get(verify=verify_ssl, url=url, json=input_json)

    return response
