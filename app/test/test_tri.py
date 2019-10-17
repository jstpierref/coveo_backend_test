import unittest
from app.engine.tri import Tri

class TestIndexing(unittest.TestCase):

    def test_tri_add_word(self):
        tri = Tri()
        tri.add_word(1, "test")

        self.assertEqual(list(tri.root.get_children().keys())[0], 't')
        next_node = tri.root.get_children()['t']
        self.assertEqual(list(next_node.get_children().keys())[0], 'e')
        next_node = next_node.get_children()['e']
        self.assertEqual(list(next_node.get_children().keys())[0], 's')
        next_node = next_node.get_children()['s']
        self.assertEqual(list(next_node.get_children().keys())[0], 't')

        self.assertEqual(len(tri.root.get_children().keys()), 1)

    def test_tri_add_words(self):
        tri = Tri()
        tri.add_words([(1, "test"), (2, "tester")])
        self.assertEqual(list(tri.root.get_children().keys())[0], 't')
        self.assertEqual(tri.autocomplete("test"), [(1, 'test'), (2, 'tester')])

    def test_tri_autocomplete(self):
        tri = Tri()
        tri.add_word(1, "test")
        tri.add_word(2, "tester")
        tri.add_word(3, "team")

        self.assertEqual(tri.autocomplete("t"), [(1, 'test'), (2, 'tester'), (3, 'team')])
        self.assertEqual(tri.autocomplete("te"), [(1, 'test'), (2, 'tester'), (3, 'team')])
        self.assertEqual(tri.autocomplete("tes"), [(1, 'test'), (2, 'tester')])
        self.assertEqual(tri.autocomplete("test"), [(1, 'test'), (2, 'tester')])
        self.assertEqual(tri.autocomplete("tester"), [(2, 'tester')])
        self.assertEqual(tri.autocomplete("tested"), [])

    def test_tri_duplicates(self):
        tri = Tri()
        tri.add_word(1, "test")       
        tri.add_word(2, "test")    
        tri.add_word(3, "team")    
        self.assertEqual(tri.autocomplete("t"), [(1, "test"), (2, "test"), (3, "team")])  

if __name__ == '__main__':
    unittest.main()
