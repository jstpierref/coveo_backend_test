import unittest
from app.engine.score import (indexer, 
                              AdditionalData,
                              ScoreInterface)

from app.engine.query import Query

class EngineTestCase(unittest.TestCase):
    """This class represents the engine test case"""

    def test_indexer(self):
        """Test indexer"""
        self.assertEqual(indexer.city_data[5885383]["name"], "Anmore")

    def test_additional_data(self):
        """Test hash map for additional data"""
        unique_ids = [5884083, 5884467, 5884473] 
        results = AdditionalData.run(unique_ids)
        self.assertEqual(results[5884083]["name"], "Alma, QC, Canada")

    def test_interface(self):
        """Test interface"""
        q = Query({"q": "Montréal"})
        results = ScoreInterface().run(q)
        names = [i["name"] for i in results]
        self.assertTrue("Montréal, QC, Canada" in names)

if __name__ == "__main__":
    unittest.main()