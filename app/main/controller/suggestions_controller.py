from flask import request, Response, abort
from flask_restplus import Resource, Namespace

import unidecode
import json

from app.engine.query import Query
from app.engine.score import ScoreInterface


api = Namespace("suggestions", description="Get city suggestions from keyword")

query_params = {
    "q": "Query keyword", 
    "lattitude": "City lattitude", 
    "longitude": "City longitude"
}

@api.route("")
@api.doc(params=query_params)
class Suggestions(Resource):
    @api.doc("get_suggestions_from_keyword")
    @api.response(200, 'Success')
    def get(self):
        if not request.args.get("q"):
            abort(404, "Mandatory parameter `q` missing from current request")
        
        query = Query(request.args)
        data = ScoreInterface().run(query)

        response = {
            "suggestions": data
        }

        response = json.dumps(response, ensure_ascii=False)
        response = Response(response, 
            content_type="application/json; charset=utf-8")
        return response

    @api.doc(responses={403: "Not Authorized"})
    def post(self):
        api.abort(403)