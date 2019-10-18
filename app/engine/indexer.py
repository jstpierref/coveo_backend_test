from app.engine.parser import Parser
from app.engine.trie import Trie

import app.engine.utils as utils


class Indexer:
    """
    Class responsible for indexing the parsed data in appropriate data structures
    for fast look-ups. General `city_data` are stored in a hash table and
    query keywords in a trie called `trie` (that supports auto-completion by nature).

    Attributes:
        filepath (str):  path of tsv file (only format supported)
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.city_data = None
        self.trie = Trie()

        self._parse()
        # methods to build the trie, called once.
        self._extract_city_names()
        self._supplement_city_names()
        self._build_trie()

    def _parse(self):
        parser = Parser(self.filepath)
        self.city_data = parser.run()

    def _extract_city_names(self):
        """Goes over parsed data to extract city names and alt names"""
        names = []
        for key, value in self.city_data.items():
            names.extend([(key, utils.standardize(value['name']), 'name', 0)])
            if value['alt_name']:
                alt_names = value['alt_name'].split(',')
                names.extend([(key, utils.standardize(n), 'alt_name', 0) \
                    for n in alt_names])
        self.city_names =  names

    def _supplement_city_names(self):
        """
        Update city names with more keywords like decoded UTF-8 and
        substrings in city names (like 'york' from 'new-york', etc.)
        """
        city_names_buffer = []
        for city in self.city_names:
            idx = city[0]
            name = city[1]
            name_type = city[2]
            decoded_name = utils.decode(name)
            if decoded_name != name:
                city_names_buffer.append((idx, decoded_name, name_type, 0))
            if " " in name or "-" in name:
                deconstructed_string = utils.deconstruct_string(name)
                for i, word in enumerate(deconstructed_string):
                    city_names_buffer.append((idx, word, 'sub_name', i))

        self.city_names.extend(city_names_buffer)

    def _build_trie(self):
        self.trie.add_words(self.city_names)

    def lookup(self, word):
        return self.trie.autocomplete(word)



