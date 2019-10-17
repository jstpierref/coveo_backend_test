from flask import Flask
from .config import config_table

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_table[config_name])
    return app