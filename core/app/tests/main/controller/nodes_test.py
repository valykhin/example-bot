import unittest
import json
import sys

from core.app import create_app
from core.app.settings import TestConfig


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig).test_client()

    def test_nodes_list(self):
        response = self.app.get('/api/nodes')
        result = json.loads(response.get_data().decode(sys.getdefaultencoding()))
        self.assertEqual(result[0]['address'], '45.67.230.163:8000')
        self.assertEqual(result[0]['country_code'], 'RU')
        self.assertEqual(result[0]['name'], 'russian')


if __name__ == "__main__":
    unittest.main()
