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

    return manual(url, callback=None)


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

    return manual(url, callback)


def manual(requestURL, callback=None):
    """
        This fuction is used by load_forecast OR by users to manually
        construct the URL for an API call.
    """

    if callback is None:
        return get_forecast(requestURL)
    else:
        thread = threading.Thread(target=load_async,
                                  args=(requestURL, callback))
        thread.start()


def get_forecast(requestURL):
    forecastio_reponse = requests.get(requestURL)

    json = forecastio_reponse.json()
    headers = forecastio_reponse.headers

    return Forecast(json, forecastio_reponse, headers)


def load_async(url, callback):
    callback(get_forecast(url))
