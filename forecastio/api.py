import requests
import threading

from forecastio.models import Forecast

CONST_TIMEOUT = 3.0


def load_forecast(key, lat, lng, time=None, units="auto", lang="en",
                  lazy=False, callback=None, timeout=CONST_TIMEOUT):
    """
        This function builds the request url and loads some or all of the
        needed json depending on lazy is True

        inLat:   The latitude of the forecast
        inLong:  The longitude of the forecast
        time:    A datetime.datetime object representing the desired time of
                 the forecast. If no timezone is present, the API assumes local
                 time at the provided latitude and longitude.
        units:   A string of the preferred units of measurement, "auto" id
                 default. also us,ca,uk,si is available
        lang:    Return summary properties in the desired language
        lazy:    Defaults to false.  The function will only request the json
                 data as it is needed. Results in more requests, but
                 probably a faster response time (I haven't checked)
        timeout: The timeout in seconds. Defaults to 3 seconds.
    """
    if time is None:
        url = 'https://api.darksky.net/forecast/%s/%s,%s' \
              '?units=%s&lang=%s' % (key, lat, lng, units, lang)
    else:
        url_time = time.replace(microsecond=0).isoformat()  # API returns 400 for microseconds
        url = 'https://api.darksky.net/forecast/%s/%s,%s,%s' \
              '?units=%s&lang=%s' % (key, lat, lng, url_time, units, lang)

    if lazy is True:
        baseURL = "%s&exclude=%s" % (url,
                                     'minutely,currently,hourly,'
                                     'daily,alerts,flags')
    else:
        baseURL = url

    return manual(baseURL, callback=callback, timeout=timeout)


def manual(requestURL, callback=None, timeout=CONST_TIMEOUT):
    """
        This function is used by load_forecast OR by users to manually
        construct the URL for an API call.
    """

    if callback is None:
        return get_forecast(requestURL, timeout)
    else:
        thread = threading.Thread(target=load_async,
                                  args=(requestURL, callback, timeout))
        thread.start()


def get_forecast(requestURL, timeout=CONST_TIMEOUT):
    forecastio_reponse = requests.get(requestURL, timeout=timeout)
    forecastio_reponse.raise_for_status()

    json = forecastio_reponse.json()
    headers = forecastio_reponse.headers

    return Forecast(json, forecastio_reponse, headers)


def load_async(url, callback, timeout=CONST_TIMEOUT):
    callback(get_forecast(url, timeout=timeout))
