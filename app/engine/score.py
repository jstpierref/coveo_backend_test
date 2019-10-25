import os
import math
from dotenv import load_dotenv
load_dotenv()

from app.engine.indexer import Indexer
import app.engine.utils as utils

indexer = Indexer(os.getenv("APP_DATA_PATH", "data/cities_canada-usa.tsv"))

class QueryScoreProcessor:
    """Class calculating query/keyword match score based on mulitple assumptions
    such as:

    1. `search_result_length_value`: gives higher score if query and found 
        keyword have similar length
    2.  `search_result_type_value`: gives higher score if query corresponds to
        an official name (`name`) than an alternative name (`alt_name`) or a
        subname of city name (`sub_name`) (e.g.: 'york' is a subname of 'new-york')
    3. `search_result_position_value`: if query is a subname of a city name, 
        gives higher score if the substring is located at the beginning of city 
        name (e.g.: 'new' and 'york' have positions 0 and 1 respectively 
        in 'new-york')
    """
    @classmethod
    def run(cls, query_word):
        search_results = indexer.lookup(query_word)
        unique_ids = list(set([i[0] for i in search_results]))
        scores = cls.apply_logic(search_results, query_word)
        return unique_ids, scores

    @staticmethod
    def apply_logic(search_results, query_word):
        def search_result_length_value(word, query_word):
            return len(query_word)/len(word)

        def search_result_type_value(rtype):
            rtype_values = {
            "name": 1.,
            "sub_name": 0.5,
            "alt_name": 0.5
            }
            return rtype_values[rtype]

        def search_result_position_value(position):
            return 1/(position+1.)  

        def check_validity(length_score, query_word, word):
            # query_word = 
            if query_word in word:
                return length_score
            return 0

        search_result_buffer = {}

        for current_rtype in ("name","sub_name","alt_name"):
            for search_result in search_results:
                idx, word, rtype, pos = search_result
                if rtype == current_rtype and idx not in search_result_buffer.keys():
                    search_result_buffer[idx] = (word, rtype, pos)

        search_results = search_result_buffer

        scores = {}
        for idx in search_results.keys():
            length_score = search_result_length_value(search_results[idx][0], query_word)
            length_score = check_validity(length_score, query_word, search_results[idx][0])
            rtype_score = search_result_type_value(search_results[idx][1])
            position_score = search_result_position_value(search_results[idx][2])
            scores[idx] = (length_score, rtype_score, position_score)

        return scores

class GeoScoreProcessor:
    """Class calculating the normalized score from query and matched cities
    geo-location.

    Distance between points is first calculated in km, assuming the Earth is 
    a perfect sphere, and a simple math.exp(-d/300) is applied.
    """
    @classmethod
    def run(cls, ids, lat1, lon1):
        scores = {}
        for i in ids:
            data = indexer.city_data[i]
            lat2 = data["lat"]
            lon2 = data["long"]
            d = utils.calculate_distance(lat1, lon1, lat2, lon2)
            scores[i] = cls.apply_logic(d)
        return scores
        
    @staticmethod
    def apply_logic(x):
        return math.exp(-x/300)

class AdditionalData:
    """Aggregates additional data for the API response"""
    field_name_cast = {}
    field_value_cast = {}

    @classmethod
    def run(cls, ids):
        data = {}
        for i in ids:
            data[i] = {}
            name = indexer.city_data[i]["name"]
            country = indexer.city_data[i]["country"]
            admin = indexer.city_data[i]["admin1"]
            data[i]["name"] = "{}, {}, {}".format(name, admin, country)
            data[i]["latitude"] = indexer.city_data[i]["lat"]
            data[i]["longitude"] = indexer.city_data[i]["long"]
        return data


class ScoreInterface:
    """Class exposing indexer and scoring logic to API routes.
    """
    def run(self, query):
        geo_scores = None
        word = query.q

        unique_ids, query_scores = QueryScoreProcessor.run(word)
        additional_data = AdditionalData.run(unique_ids)

        if query.lat and query.lon:
            geo_scores = GeoScoreProcessor.run(unique_ids, query.lat, query.lon)

        global_scores = self.calculate_global_score(query_scores, geo_scores)

        returned_data = additional_data
        for idx in returned_data.keys():
            returned_data[idx]["score"] = round(global_scores[idx],2)

        returned_data = list(returned_data.values())
        returned_data.sort(key=lambda x: x["score"], reverse=True)
        return returned_data

    @staticmethod
    def calculate_global_score(query_scores, geo_scores):
        scores = {}
        if geo_scores:
            for idx in query_scores.keys():
                qs = query_scores[idx]
                gs = geo_scores[idx]
                scores[idx] = 0.3*qs[0] + 0.1*qs[1] + 0.1*qs[2] + 0.5*gs
        else:
            for idx in query_scores.keys():
                qs = query_scores[idx]
                scores[idx] = 0.4*qs[0] + 0.3*qs[1] + 0.3*qs[2]
        return scores

