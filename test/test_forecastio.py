import json
import unittest
import forecastio
from mock import MagicMock

class forecastio_test(unittest.TestCase):
    def setUp(self):
        mock_json = open('test/test.json').read()
        mock_data = json.loads(mock_json)
        fc_mock_res = forecastio.models.Forecast(mock_data, '', '')
        forecastio.load_forecast = MagicMock(return_value=fc_mock_res)
        api_key = "foo"
        lat = 50.0
        lng = 10.0
        self.fc = forecastio.load_forecast(api_key, lat, lng)

    def test_001(self):
        fc_cur = self.fc.currently()
        self.assertEqual(fc_cur.temperature, 55.81)
