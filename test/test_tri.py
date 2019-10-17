import unittest
from src.tri import Tri

class TestIndexing(unittest.TestCase):

    def test_add_word(self):
        tri = Tri()
        tri.add_word(1, "test")

        # tri.dps_print()

        self.assertEqual(list(tri.root.get_children().keys())[0], 't')
        next_node = tri.root.get_children()['t']
        self.assertEqual(list(next_node.get_children().keys())[0], 'e')
        next_node = next_node.get_children()['e']
        self.assertEqual(list(next_node.get_children().keys())[0], 's')
        next_node = next_node.get_children()['s']
        self.assertEqual(list(next_node.get_children().keys())[0], 't')

        self.assertEqual(len(tri.root.get_children().keys()), 1)

    def test_get_table_elements(self):
        tri = Tri()
        tri.add_word(1, "test")
        tri.add_word(2, "tester")
        tri.add_word(3, "team")

        self.assertEqual(tri.get_table_elements("t"), [1,2,3])
        self.assertEqual(tri.get_table_elements("te"), [1,2,3])
        self.assertEqual(tri.get_table_elements("tes"), [1,2])
        self.assertEqual(tri.get_table_elements("test"), [1,2])
        self.assertEqual(tri.get_table_elements("tester"), [2])
        self.assertEqual(tri.get_table_elements("tested"), [])
        # self.assertTrue('FOO'.isupper())
        # self.assertFalse('Foo'.isupper())

    def test_duplicates(self):
        tri = Tri()
        tri.add_word(1, "test")       
        tri.add_word(2, "test")    
        # self.assertEqual(s.split(), ['hello', 'world'])

if __name__ == '__main__':
    unittest.main()
