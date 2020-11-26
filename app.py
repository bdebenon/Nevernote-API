import json

from flask import Flask, request, send_file
from flask_cors import CORS

from helpers.flask import params_to_dict
from helpers.http import http_response
from routes.notebooks.get import notebooks_get
from routes.notebooks.post import notebooks_post
from routes.notes.get import notes_get
from routes.notes.post import notes_post

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
            raise Exception("Invalid Request Type.")
    except Exception as e:
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
            raise Exception("Invalid Request Type.")
    except Exception as e:
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
            raise Exception("Invalid Request Type.")
    except Exception as e:
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
            raise Exception("Invalid Request Type.")
    except Exception as e:
        return http_response.http_failure_response(
            404, http_response.InternalResponseCode.invalid_request_type, str(e)
            )


if __name__ == "__main__":
    # Intended to be run on a server at the IP 'www.occuply.io' is pointing to
    # app.run(ssl_context=('ssl/multapply_cert.pem', 'ssl/multapply_key.pem'), host='0.0.0.0', port="443")
    pass
    # PARAMS for FLASK through PyCharm (Additional Options)
    # --cert ssl/fullchain.pem --key ssl/privkey.pem --port 443 --host 0.0.0.0
    # --cert /etc/letsencrypt/live/www.multapply.io/fullchain.pem --key /etc/letsencrypt/live/www.multapply.io/privkey.pem --port 443 --host 0.0.0.0
