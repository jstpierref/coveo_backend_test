import unittest
from app.engine.trie import trie

class TestIndexing(unittest.TestCase):

    def test_trie_add_word(self):
        trie = trie()
        trie.add_word(1, "test")

        self.assertEqual(list(trie.root.get_children().keys())[0], 't')
        next_node = trie.root.get_children()['t']
        self.assertEqual(list(next_node.get_children().keys())[0], 'e')
        next_node = next_node.get_children()['e']
        self.assertEqual(list(next_node.get_children().keys())[0], 's')
        next_node = next_node.get_children()['s']
        self.assertEqual(list(next_node.get_children().keys())[0], 't')

        self.assertEqual(len(trie.root.get_children().keys()), 1)

    def test_trie_add_words(self):
        trie = trie()
        trie.add_words([(1, "test"), (2, "tester")])
        self.assertEqual(list(trie.root.get_children().keys())[0], 't')
        self.assertEqual(trie.autocomplete("test"), [(1, 'test'), (2, 'tester')])

    def test_trie_autocomplete(self):
        trie = trie()
        trie.add_word(1, "test")
        trie.add_word(2, "tester")
        trie.add_word(3, "team")

        self.assertEqual(trie.autocomplete("t"), [(1, 'test'), (2, 'tester'), (3, 'team')])
        self.assertEqual(trie.autocomplete("te"), [(1, 'test'), (2, 'tester'), (3, 'team')])
        self.assertEqual(trie.autocomplete("tes"), [(1, 'test'), (2, 'tester')])
        self.assertEqual(trie.autocomplete("test"), [(1, 'test'), (2, 'tester')])
        self.assertEqual(trie.autocomplete("tester"), [(2, 'tester')])
        self.assertEqual(trie.autocomplete("tested"), [])

    def test_trie_duplicates(self):
        trie = trie()
        trie.add_word(1, "test")       
        trie.add_word(2, "test")    
        trie.add_word(3, "team")    
        self.assertEqual(trie.autocomplete("t"), [(1, "test"), (2, "test"), (3, "team")])  

if __name__ == '__main__':
    unittest.main()
