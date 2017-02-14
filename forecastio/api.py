import requests

from geopy import geocoders

from forecastio.utils import build_url
from forecastio.models import Forecast


def load(key, lat, lng, time=None, **kawrgs):
    """
        This function builds the request url and loads the response data

        lat:  The latitude of the forecast
        long: The longitude of the forecast
        time:   A unix timestamp representing the desired UTC time of
                the forecast.
    """

    url = build_url(key, lat, lng, time, url_params=kawrgs)

    return manual(url)


def geocode(key, address, time=None, google_api_key=None, **kawrgs):
    """
        address: A string address to then be geocoded into lnt/long.
        google_api_key: Google API key for business users.
    """

    location, (lat, lng) = geocoders.GoogleV3(api_key=google_api_key).geocode(address)

    url = build_url(key, lat, lng, time, url_params=kawrgs)

    return manual(url)


def manual(requestURL):
    """
        This fuction is used by load OR by users to manually
        construct the URL for an API call.
    """

    return _forecast_factory(requestURL)


def _forecast_factory(requestURL):
    dark_sky_response = requests.get(requestURL, timeout=30)
    dark_sky_response.raise_for_status()

    json = dark_sky_response.json()
    headers = dark_sky_response.headers

    return Forecast(json, dark_sky_response, headers)
