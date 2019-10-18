import unittest
import app.engine.utils as utils

class UtilsTestCase(unittest.TestCase):
    """This class represents the utils test case"""

    def test_null_distance(self):
        """Test null distances"""
        d = utils.calculate_distance(30, 30, 30, 30)
        self.assertEqual(d, 0)

    def test_distance(self):
        """Test distances"""
        d = utils.calculate_distance(30, 30, 40, 40)
        self.assertEqual(round(d), 1436)

    def test_distance(self):
        """Test string deconstructions"""
        s = "New-York city"
        self.assertEqual(utils.deconstruct_string(s), ["New","York","city"])

    def test_utf8_decoding(self):
        """Test utf8 decoding and string standardization"""
        s = "Montréal"
        self.assertEqual(utils.standardize(utils.decode(s)),"montreal")


if __name__ == "__main__":
    unittest.main()