from flask_restplus import Api
from flask import Blueprint

from .main.controller.suggestions_controller import api as suggestions_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Coveo Backend Test',
          version='1.0',
          description='Swagger documentation'
          )

api.add_namespace(suggestions_ns, path='/suggestions')