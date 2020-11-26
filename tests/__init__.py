from config import config

params = config("api_connection_settings")


def get_api_endpoint():
    # Set API Endpoint
    if params["api_type"] == "Local":
        api_endpoint = f"{params['connection_prefix']}{params['local_url']}:{params['api_port']}"
    else:
        api_endpoint = f"{params['connection_prefix']}{params['aws_url']}:{params['api_port']}"
    return api_endpoint


def get_verify_ssl():
    # Set API Endpoint
    if params["verify_ssl"] == "True":
        verify_ssl = True
    else:
        verify_ssl = False
    return verify_ssl


if __name__ == "__main__":
    testing_api_endpoint = get_api_endpoint()
    print(f'API Endpoint being tested: {testing_api_endpoint}')
