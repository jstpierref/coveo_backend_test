import unittest
import os
import json
from app.main import create_app
from app.blueprint import blueprint

class SuggestionsTestCase(unittest.TestCase):
    """This class represents the suggetsions test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("test")
        self.app.register_blueprint(blueprint)
        self.app.app_context().push()
        self.client = self.app.test_client

    def test_empty_suggestions(self):
        """Test API returns empty suggestions (GET request)"""
        res = self.client().get('/suggestions?q=light_sabers_exist')
        self.assertEqual(res.status_code, 200)
        self.assertEqual({"suggestions": []}, json.loads(res.data))

    def test_direct_suggestions(self):
        """Test API returns direct suggestions (GET request)"""
        res = self.client().get('/suggestions?q=Montréal')

        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.data)["suggestions"]
        names = [i['name'] for i in res_data]
        self.assertTrue('Montréal, QC, Canada' in names)
        self.assertTrue('Montréal-Ouest, QC, Canada' in names)

    def test_sub_name_suggestions(self):
        """Test API returns 'New York' from 'york' (GET request)"""
        res = self.client().get('/suggestions?q=york')

        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.data)["suggestions"]
        names = [i['name'] for i in res_data]
        self.assertTrue('New York City, NY, USA' in names)

    def test_autocomplete_suggestions(self):
        """Test API returns autocomplete suggestions (GET request)"""

        res = self.client().get('/suggestions?q=Qué')

        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.data)["suggestions"]
        names = [i['name'] for i in res_data]
        self.assertTrue('Québec, QC, Canada' in names)


if __name__ == "__main__":
    unittest.main()