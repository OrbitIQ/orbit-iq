from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register the blueprints
from routes.confirmed import confirmed_subpath
app.register_blueprint(confirmed_subpath, url_prefix='/confirmed')

from routes.edit import edit_subpath
app.register_blueprint(edit_subpath, url_prefix='/edit')

def print_routes(app):
    print("Routes defined in the application:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

if __name__ == '__main__':
    print_routes(app)
    app.run(host='0.0.0.0', port=8080, debug=True)