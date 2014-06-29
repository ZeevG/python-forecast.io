import requests
import time as Time
import threading
from geopy import geocoders

from forecastio.models import Forecast


def load_forecast(key, inLat=None, inLong=None, address=None,
                  time=None, units="auto", lazy=False, callback=None):

    """
        This function builds the request url and loads some or all of the
        needed json depending on lazy is True

        inLat:  The latitude of the forecast
        inLong: The longitude of the forecast
        address: A string address to then be geocoded into lnt/long.
                 Requires geopy.
        time:   A datetime.datetime object representing the desired time of
                the forecast
        units:  A string of the preferred units of measurement, "auto" id
                default. also us,ca,uk,si is available
        lazy:   Defaults to false.  The function will only request the json
                data as it is needed. Results in more requests, but
                probably a faster response time (I haven't checked)
    """

    lat = inLat
    lng = inLong
    time = time
    
    if address:
        location, (lat, lng) = geocoders.GoogleV3().geocode(address)

    if time is None:
        url = 'https://api.forecast.io/forecast/%s/%s,%s' \
              '?units=%s' % (key, lat, lng, units,)
    else:
        url_time = str(int(Time.mktime(time.timetuple())))
        url = 'https://api.forecast.io/forecast/%s/%s,%s,%s' \
              '?units=%s' % (key, lat, lng, url_time,
              units,)

    if lazy is True:
        baseURL = "%s&exclude=%s" % (url,
                                     'minutely,currently,hourly,'
                                     'daily,alerts,flags')
    else:
        baseURL = url

    if callback is None:
        return make_forecast(make_request(baseURL))
    else:
        thr = threading.Thread(target=load_async, args=(baseURL,),
                               kwargs={'callback': callback})
        thr.start()


def make_forecast(response):
    return Forecast(response.json(), response, response.headers)


def make_request(url):
    return requests.get(url)


def load_async(url, callback):
    callback(make_forecast(make_request(url)))
