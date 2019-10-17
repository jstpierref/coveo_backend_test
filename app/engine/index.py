from parser import Parser
from trie import Trie


def norm(name):
	return name.lower().strip()

class Index:
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
		for key, value in self.city_data.items():
			current_names = [value['name']]
			if value['alt_name']:
				current_names.extend(value['alt_name'].split(','))
			names.extend([(key, norm(n)) for n in current_names])
		self.city_names =  names

	def _build_trie(self):
		self.trie.add_words(self.city_names)

	def lookup(self, word):
		return self.trie.autocomplete(word)
## dont forget to remove spaces before after names and comma

p = Index("data/cities_canada-usa.tsv")
# print(p.city_names)

print(p.lookup('mont'))
