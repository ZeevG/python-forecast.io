import forecastio

import os
import unittest
import responses
import requests
try:
    import urlparse
except:
    import urllib.parse as urlparse


from datetime import datetime
from nose.tools import raises


class EndToEnd(unittest.TestCase):

    def setUp(self):
        self.api_key = os.environ.get("FORECASTIO_API_KEY")

        self.lat = 52.370235
        self.lng = 4.903549

        self.time = datetime(2015, 2, 27, 6, 0, 0)

    def test_with_time(self):

        forecast = forecastio.load(
            self.api_key, self.lat,
            self.lng, time=self.time
        )
        self.assertEqual(forecast.response.status_code, 200)

    def test_without_time(self):

        forecast = forecastio.load(
            self.api_key, self.lat, self.lng
        )
        self.assertEqual(forecast.response.status_code, 200)

    def test_invalid_key(self):
        self.api_key = 'not a real key'

        try:
            forecastio.load(
                self.api_key, self.lat, self.lng
            )

            self.assertTrue(False)  # the previous line should throw an exception
        except requests.exceptions.HTTPError as e:
            self.assertTrue(e.response.status_code == 404)

    def test_invalid_param(self):
        self.lat = ''

        try:
            forecastio.load(
                self.api_key, self.lat, self.lng
            )

            self.assertTrue(False)  # the previous line should throw an exception
        except requests.exceptions.HTTPError as e:
            self.assertTrue(e.response.status_code == 404)

class BasicFunctionality(unittest.TestCase):

    @responses.activate
    def setUp(self):
        URL = "https://api.darksky.net/forecast/foo/50.0,10.0"
        responses.add(responses.GET, URL,
                      body=open('tests/fixtures/test.json').read(),
                      status=200,
                      content_type='application/json',
                      match_querystring=True)

        api_key = "foo"
        lat = 50.0
        lng = 10.0
        self.fc = forecastio.load(api_key, lat, lng)

        self.assertEqual(responses.calls[0].request.url, URL)

    def test_current_temp(self):
        fc_cur = self.fc.currently()
        self.assertEqual(fc_cur.temperature, 55.81)

    def test_datablock_summary(self):

        hourl_data = self.fc.hourly()
        self.assertEqual(hourl_data.summary, "Drizzle until this evening.")

    def test_datablock_icon(self):

        hourl_data = self.fc.hourly()
        self.assertEqual(hourl_data.icon, "rain")

    def test_datablock_not_available(self):

        minutely = self.fc.minutely()
        self.assertEqual(minutely.data, [])

    def test_datapoint_number(self):

        hourl_data = self.fc.hourly()
        self.assertEqual(len(hourl_data.data), 49)

    def test_datapoint_temp(self):

        daily = self.fc.daily()
        self.assertEqual(daily.data[0].temperatureMin, 50.73)

    def test_datapoint_string_repr(self):

        currently = self.fc.currently()

        self.assertEqual(
            "{}".format(currently),
            "<ForecastioDataPoint instance: Overcast at 2014-05-28 08:27:39>"
        )

    def test_datablock_string_repr(self):

        hourly = self.fc.hourly()

        self.assertEqual(
            "{}".format(hourly),
            "<ForecastioDataBlock instance: Drizzle until this evening. "
            "with 49 ForecastioDataPoints>"
        )

    @raises(forecastio.utils.PropertyUnavailable)
    def test_datapoint_attribute_not_available(self):
        daily = self.fc.daily()
        daily.data[0].notavailable

    def test_apparentTemperature(self):
        hourly = self.fc.hourly()
        apprentTemp = hourly.data[0].apparentTemperature

        self.assertEqual(apprentTemp, 55.06)

    def test_alerts_length(self):
        alerts = self.fc.alerts()
        self.assertEqual(len(alerts), 0)


class UsingOptions(unittest.TestCase):

    @responses.activate
    def test_options(self):
        URL = "https://api.darksky.net/forecast/foo/50.0,10.0?units=auto&lang=es"
        responses.add(responses.GET, URL,
                      body=open('tests/fixtures/test.json').read(),
                      status=200,
                      content_type='application/json',
                      match_querystring=True)

        api_key = "foo"
        lat = 50.0
        lng = 10.0
        options = {'units': 'auto', 'lang': 'es'}
        self.fc = forecastio.load(api_key, lat, lng, **options)

        # Check the expected url was called.
        actualUrl = urlparse.urlparse(responses.calls[0].request.url)
        expectedUrl = urlparse.urlparse(URL)
        self.assertEqual(expectedUrl, actualUrl)

        # Check the resulting forecast object is accessible
        fc_cur = self.fc.currently()
        self.assertEqual(fc_cur.temperature, 55.81)


class Geocode(unittest.TestCase):

    @responses.activate
    def test_geocoding(self):
        URL = "https://api.darksky.net/forecast/foo/48.7904472,11.4978895"
        responses.add(responses.GET, URL,
                      body=open('tests/fixtures/test.json').read(),
                      status=200,
                      content_type='application/json',
                      match_querystring=True)

        api_key = "foo"
        address = 'Bavaria, Germany'
        self.fc = forecastio.geocode(api_key, address)
        self.assertEqual(responses.calls[0].request.url, URL)

        fc_cur = self.fc.currently()
        self.assertEqual(fc_cur.temperature, 55.81)


class ForecastsWithAlerts(unittest.TestCase):

    @responses.activate
    def setUp(self):
        URL = "https://api.darksky.net/forecast/foo/50.0,10.0"
        responses.add(responses.GET, URL,
                      body=open('tests/fixtures/test_with_alerts.json').read(),
                      status=200,
                      content_type='application/json',
                      match_querystring=True)

        api_key = "foo"
        lat = 50.0
        lng = 10.0
        self.fc = forecastio.load(api_key, lat, lng)

    def test_alerts_length(self):
        alerts = self.fc.alerts()
        self.assertEqual(len(alerts), 2)

    def test_alert_title(self):
        alerts = self.fc.alerts()
        first_alert = alerts[0]

        self.assertEqual(
            first_alert.title,
            "Excessive Heat Warning for Inyo, CA"
        )

    def test_alert_uri(self):
        alerts = self.fc.alerts()
        first_alert = alerts[0]

        self.assertEqual(
            first_alert.uri,
            "http://alerts.weather.gov/cap/wwacapget.php"
            "?x=CA125159BB3908.ExcessiveHeatWarning."
            "125159E830C0CA.VEFNPWVEF.8faae06d42ba631813492a6a6eae41bc"
        )

    def test_alert_time(self):
        alerts = self.fc.alerts()
        first_alert = alerts[0]

        self.assertEqual(
            first_alert.time,
            1402133400
        )

    @raises(forecastio.utils.PropertyUnavailable)
    def test_alert_property_does_not_exist(self):
        alerts = self.fc.alerts()
        first_alert = alerts[0]

        first_alert.notarealproperty

    def test_alert_string_repr(self):
        alerts = self.fc.alerts()
        first_alert = alerts[0]

        self.assertEqual(
            first_alert.time,
            1402133400
        )


class BasicManualURL(unittest.TestCase):

    @responses.activate
    def setUp(self):

        URL = "http://test_url.com/"
        responses.add(responses.GET, URL,
                      body=open('tests/fixtures/test.json').read(),
                      status=200,
                      content_type='application/json',
                      match_querystring=True)

        self.forecast = forecastio.manual("http://test_url.com/")

    def test_current_temp(self):

        fc_cur = self.forecast.currently()
        self.assertEqual(fc_cur.temperature, 55.81)

    def test_datablock_summary(self):

        hourl_data = self.forecast.hourly()
        self.assertEqual(hourl_data.summary, "Drizzle until this evening.")
