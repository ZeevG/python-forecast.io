import requests
import threading

from forecastio.utils import build_url
from forecastio.models import Forecast


def load_forecast(key, lat, lng, time=None, options=None):
    """
        This function builds the request url and loads some or all of the
        needed json depending on lazy is True

        inLat:  The latitude of the forecast
        inLong: The longitude of the forecast
        time:   A datetime.datetime object representing the desired time of
                the forecast
    """

    url = build_url(key, lat, lng, time, options)

    return manual(url)


def load_forecast_async(key, lat, lng, callback, time=None, options=None):
    """
        This function builds the request url and loads some or all of the
        needed json depending on lazy is True

        inLat:  The latitude of the forecast
        inLong: The longitude of the forecast
        time:   A datetime.datetime object representing the desired time of
                the forecast
    """

    url = build_url(key, lat, lng, time, options)

    return manual_async(url, callback)


def manual(requestURL):
    """
        This fuction is used by load_forecast OR by users to manually
        construct the URL for an API call.
    """

    return _make_request(requestURL)


def manual_async(requestURL, callback):
    """
        This fuction is used by load_forecast_async OR by users to manually
        construct the URL for an API call.
    """

    thread = threading.Thread(target=_async_wrapper,
                              args=(requestURL, callback))
    thread.start()


def _make_request(requestURL):
    forecastio_reponse = requests.get(requestURL)

    json = forecastio_reponse.json()
    headers = forecastio_reponse.headers

    return Forecast(json, forecastio_reponse, headers)


def _async_wrapper(url, callback):
    callback(_make_request(url))
