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


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def deconstruct_string(string):
    """e.g: splits 'New-York city' into ['New', 'York', 'city']"""
    substring_buffer = ""
    deconstructed_string = []
    for char in string:
        if char == " " or char == "-":
            deconstructed_string.append(substring_buffer)
            substring_buffer = ""
        else:
            substring_buffer += char
    if substring_buffer:
        deconstructed_string.append(substring_buffer)
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

def standardize(name):
    return name.lower().strip()
    
def decode(name):
    name = unidecode_string(name)
    if "'" in name or "`" in name or "[?]" in name:
        name = "".join(name.split("'"))
        name = "".join(name.split("`"))
        name = "".join(name.split("[?]"))
    return name

