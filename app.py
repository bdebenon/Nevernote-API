import argparse
import json

from flask import Flask, request, send_file
from flask_cors import CORS

from helpers.flask import params_to_dict
from helpers.http import http_response
from routes.notebooks.get import notebooks_get
from routes.notebooks.post import notebooks_post
from routes.notes.get import notes_get
from routes.notes.post import notes_post
from helpers.exceptions import InvalidFlaskRoute

app = Flask(__name__)
CORS(app)


# documentation_command:ignore_next_route
# default route
@app.route(rule='/', methods=["GET"])
def default():
    try:
        if request.method == "GET":
            return json.dumps({"message": "Hello World!"})
        else:
            raise InvalidFlaskRoute("Invalid Request Type.")
    except InvalidFlaskRoute as e:
        return http_response.http_failure_response(
            404, http_response.InternalResponseCode.invalid_request_type, str(e)
            )


# documentation_command:ignore_next_route
# documentation
@app.route(rule='/documentation', methods=["GET"])
def documentation():
    try:
        if request.method == "GET":
            return send_file('documentation/api_documentation.html')
        else:
            raise InvalidFlaskRoute("Invalid Request Type.")
    except InvalidFlaskRoute as e:
        return http_response.http_failure_response(
            404, http_response.InternalResponseCode.invalid_request_type, str(e)
            )


# notebooks
@app.route(rule='/notebooks', methods=["GET", "POST"])
def notebooks():
    try:
        if request.method == "GET":
            return notebooks_get(**params_to_dict(request.args))
        elif request.method == "POST":
            return notebooks_post(**request.json)
        else:
            raise InvalidFlaskRoute("Invalid Request Type.")
    except InvalidFlaskRoute as e:
        return http_response.http_failure_response(
            404, http_response.InternalResponseCode.invalid_request_type, str(e)
            )


# notes
@app.route(rule='/notes', methods=["GET", "POST"])
def notes():
    try:
        if request.method == "GET":
            return notes_get(**params_to_dict(request.args))
        elif request.method == "POST":
            return notes_post(**request.json)
        else:
            raise InvalidFlaskRoute("Invalid Request Type.")
    except InvalidFlaskRoute as e:
        return http_response.http_failure_response(
            404, http_response.InternalResponseCode.invalid_request_type, str(e)
            )


if __name__ == "__main__":
    # Setup command line arguments
    arg_parser = argparse.ArgumentParser(description='Determining arguments to call correct function')
    arg_parser.add_argument("-p", "--port", dest="port", required=False, help="Specify port to run Flask on.")
    arg_parser.add_argument(
        "-i", "--ip_address", dest="ip_address", required=False, help="Specify IP to run Flask on."
        )

    # Retrieve command line arguments
    args = arg_parser.parse_args()
    ip_address = args.ip_address if args.ip_address else "0.0.0.0"
    port = args.port if args.ip_address else "80"

    # Start Flask
    app.run(host=ip_address, port=port)
