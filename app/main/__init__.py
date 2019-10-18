from flask import Flask, jsonify
from .config import config_table
import os

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_table[config_name])

    @app.route('/vars')
    def home():
        environment_variables = { key: os.environ[key] for key in os.environ.keys() }
        return jsonify(environment_variables)

    return app