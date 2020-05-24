"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""


from flask_dotenv import DotEnv
env = DotEnv(app)

from flask import jsonify
from axioms_flask.error import AxiomsError

@app.errorhandler(AxiomsError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    if ex.status_code == 401:
        response.headers[
            "WWW-Authenticate"
        ] = "Bearer realm='{}', error='{}', error_description='{}'".format(
            app.config["AXIOMS_DOMAIN"], ex.error["error"], ex.error["error_description"]
        )
    return response

from axioms_flask.decorators import has_valid_access_token, has_required_scopes

private_api = Blueprint("private_api", __name__)

@private_api.route('/private', methods=["GET"])
@has_valid_access_token
@has_required_scopes(['openid', 'profile'])
def api_private():
    return jsonify({'message': 'All good. You are authenticated!'})

from axioms_flask.decorators import has_valid_access_token, has_required_roles

role_api = Blueprint("role_api", __name__)

@role_api.route("/role", methods=["GET", "POST", "PATCH", "DELETE"])
@has_valid_access_token
@has_required_roles(["sample:role"])
    if request.method == 'POST':
        return jsonify({"message": "Sample created."})
    if request.method == 'PATCH':
        return jsonify({"message": "Sample updated."})
    if request.method == 'GET':
        return jsonify({"message": "Sample read."})
    if request.method == 'DELETE':
        return jsonify({"message": "Sample deleted."})


from axioms_flask.decorators import has_valid_access_token, has_required_permissions

permission_api = Blueprint("permission_api", __name__)

@permission_api.route("/permission", methods=["POST"])
@has_valid_access_token
@has_required_permissions(["sample:create"])
def sample_create():
    return jsonify({"message": "Sample created."})


@permission_api.route("/permission", methods=["PATCH"])
@has_valid_access_token
@has_required_permissions(["sample:update"])
def sample_update():
    return jsonify({"message": "Sample updated."})


@permission_api.route("/permission", methods=["GET"])
@has_valid_access_token
@has_required_permissions(["sample:read"])
def sample_read():
    return jsonify({"message": "Sample read."})


@permission_api.route("/permission", methods=["DELETE"])
@has_valid_access_token
@has_required_permissions(["sample:delete"])
def sample_delete():
    return jsonify({"message": "Sample deleted."})


#from flask import Flask
#app = Flask(__name__)

## Make the WSGI interface available at the top level so wfastcgi can get it.
#wsgi_app = app.wsgi_app


#@app.route('/')
#def hello():
#    """Renders a sample page."""
#    return "Hello World!"

#if __name__ == '__main__':
#    import os
#    HOST = os.environ.get('SERVER_HOST', 'localhost')
#    try:
#        PORT = int(os.environ.get('SERVER_PORT', '5555'))
#    except ValueError:
#        PORT = 5555
#    app.run(HOST, PORT)
