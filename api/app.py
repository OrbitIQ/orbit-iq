from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from flask_jwt_extended import JWTManager


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Note: on server restart the secret will change, so all tokens will be invalidated
#       forcing users to re-login
app.config['JWT_SECRET_KEY'] = os.urandom(48)
jwt = JWTManager(app)

# Register the blueprints
from routes.confirmed import confirmed_subpath
app.register_blueprint(confirmed_subpath, url_prefix='/confirmed')

from routes.edit import edit_subpath
app.register_blueprint(edit_subpath, url_prefix='/edit')

from routes.proposed import proposed_changes_subpath
app.register_blueprint(proposed_changes_subpath, url_prefix='/proposed')

from routes.authentication import authentication_subpath
app.register_blueprint(authentication_subpath, url_prefix='/auth')

def print_routes(app):
    print("Routes defined in the application:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

if __name__ == '__main__':
    print_routes(app)
    app.run(host='0.0.0.0', port=8080, debug=True)