import unittest
import responses

import forecastio

from nose.tools import raises


class BasicFunctionality(unittest.TestCase):

    @responses.activate
    def setUp(self):
        URL = "https://api.forecast.io/forecast/foo/50.0,10.0"
        responses.add(responses.GET, URL,
                      body=open('tests/fixtures/test.json').read(),
                      status=200,
                      content_type='application/json',
                      match_querystring=True)

        api_key = "foo"
        lat = 50.0
        lng = 10.0
        self.fc = forecastio.load_forecast(api_key, lat, lng)

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

    @unittest.skip("Skipping untill timezone problems are sorted")
    def test_datapoint_string_repr(self):

        currently = self.fc.currently()

        self.assertEqual(
            "{}".format(currently),
            "<ForecastioDataPoint instance: Overcast at 2014-05-28 16:27:39>"
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
    def test_units(self):
        URL = "https://api.forecast.io/forecast/foo/50.0,10.0?units=auto"
        responses.add(responses.GET, URL,
                      body=open('tests/fixtures/test.json').read(),
                      status=200,
                      content_type='application/json',
                      match_querystring=True)

        api_key = "foo"
        lat = 50.0
        lng = 10.0
        options = {'units': 'auto'}
        self.fc = forecastio.load_forecast(api_key, lat, lng, options=options)

        # Check the expected url was called.
        self.assertEqual(responses.calls[0].request.url, URL)

        # Check the resulting forecast object is accessible
        fc_cur = self.fc.currently()
        self.assertEqual(fc_cur.temperature, 55.81)


class ForecastsWithAlerts(unittest.TestCase):

    @responses.activate
    def setUp(self):
        URL = "https://api.forecast.io/forecast/foo/50.0,10.0"
        responses.add(responses.GET, URL,
                      body=open('tests/fixtures/test_with_alerts.json').read(),
                      status=200,
                      content_type='application/json',
                      match_querystring=True)

        api_key = "foo"
        lat = 50.0
        lng = 10.0
        self.fc = forecastio.load_forecast(api_key, lat, lng)

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

    @unittest.skip("Skipping untill timezone problems are sorted")
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


class BasicWithCallback(unittest.TestCase):
    pass
    """
    Would like to test this in the future
    Not sure how to handle mocking responses in a new thread yet
    """


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
