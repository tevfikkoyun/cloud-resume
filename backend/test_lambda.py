import json
from unittest import TestCase
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler

class TestVisitorCounter(TestCase):

    @patch('lambda_function.table')
    def test_returns_200(self, mock_table):
        mock_table.update_item.return_value = {
            'Attributes': {'Count': 5}
        }
        result = lambda_handler({}, {})
        self.assertEqual(result['statusCode'], 200)

    @patch('lambda_function.table')
    def test_returns_count(self, mock_table):
        mock_table.update_item.return_value = {
            'Attributes': {'Count': 5}
        }
        result = lambda_handler({}, {})
        body = json.loads(result['body'])
        self.assertEqual(body['count'], 5)

    @patch('lambda_function.table')
    def test_has_cors_header(self, mock_table):
        mock_table.update_item.return_value = {
            'Attributes': {'Count': 5}
        }
        result = lambda_handler({}, {})
        self.assertEqual(result['headers']['Access-Control-Allow-Origin'], '*')