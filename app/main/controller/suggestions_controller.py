from flask import request, Response, abort
from flask_restplus import Resource, Namespace

import unidecode
import json

from app.engine.query import Query
from app.engine.score import ScoreInterface


api = Namespace('suggestions', description='All valid suggestions')

@api.route('/')
class Suggestions(Resource):
    @api.doc('get_suggestions_from_keyword')
    def get(self):
        if not request.args.get('q'):
            abort(404)
        
        query = Query(request.args)
        data = ScoreInterface().run(query)

        response = {
            'suggestions': data
        }

        response = json.dumps(response, ensure_ascii=False)
        response = Response(response, 
            content_type="application/json; charset=utf-8")
        return response
