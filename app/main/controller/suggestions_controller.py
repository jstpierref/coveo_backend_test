from flask import request
from flask_restplus import Resource, Namespace

api = Namespace('suggestions', description='All valid suggestions')

@api.route('/')
class Suggestions(Resource):
    @api.doc('list_of_valid_suggestions')
    def get(self):
        """List all registered users"""
        return {'status': 'ok'}
