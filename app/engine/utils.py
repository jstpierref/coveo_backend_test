from math import sin, cos, sqrt, atan2, radians
import unidecode 
import googletrans

class Translator:
    """Wraps Google Translate API"""
    def __init__(self):
        self.translator = googletrans.Translator()

    def detect_language(self, string):
        return self.translator.detect(string).text

    def translate(self, string):
        return self.translator.translate(string).text 


def calculate_distance(lat_1, lon_1, lat_2, lon_2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def deconstruct_string(string):
    substring_buffer = ""
    deconstructed_string = []
    for char in string:
        if char == " " or char == "-":
            deconstructed_string.append(substring_buffer)
            substring_buffer = ""
        else:
            substring_buffer += char
    return deconstructed_string
    

def translate_if_necessary(string):
    """Translate every words to english"""
    if not string:
        return string
    if string[0] not in """abcdefghijklmnopqrstuvwxyz'"` """:
        # print(string)
        t = Translator()
        return t.translate(string)
    return string 

def unidecode_string(string):
    return unidecode.unidecode(string)
