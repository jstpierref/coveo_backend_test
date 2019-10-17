from parser import Parser
from trie import Trie
import utils
from tqdm import tqdm 

def standardize(name):
    name =  name.lower().strip()
    name =  name.lower().strip()
    # name = utils.translate_if_necessary(name)
    name = utils.unidecode_string(name)

    return name


class Indexer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.city_data = None
        self.trie = Trie()

        self._parse()
        self._extract_city_names()
        self._build_trie()

    def _parse(self):
        parser = Parser(self.filepath)
        self.city_data = parser.run()

    def _extract_city_names(self):
        names = []
        for key, value in tqdm(self.city_data.items()):
            names.extend([(key, standardize(value['name']), 'name')])
            if value['alt_name']:
                alt_names = value['alt_name'].split(',')
                names.extend([(key, standardize(n), 'alt_name') for n in alt_names])
        self.city_names =  names
        import pdb; pdb.set_trace()

    def _build_trie(self):
        self.trie.add_words(self.city_names)

    def lookup(self, word):
        return self.trie.autocomplete(word)


p = Indexer("data/cities_canada-usa.tsv")
# print(p.city_names)

print(p.lookup('mont'))



