import json
import requests
import time as Time
import urllib2
import threading

from forecastio import Forecast


def load_forecast(key, inLat, inLong, time=None, units="auto", lazy=False,
                  callback=None):

    """
        This function builds the request url and loads some or all of the
        needed json depending on lazy is True

        inLat:  The latitude of the forecast
        inLong: The longitude of the forecast
        time:   A datetime.datetime object representing the desired time of
                the forecast
        units:  A string of the preferred units of measurement, "auto" id
                default. also us,ca,uk,si is available
        lazy:   Defaults to true.  The function will only request the json
                data as it is needed. Results in more requests, but
                probably a faster response time (I haven't checked)
    """

    lat = inLat
    lng = inLong
    time = time

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
        return make_request(baseURL)
    else:
        thr = threading.Thread(target=load_async, args=(baseURL,),
                               kwargs={'callback': callback})
        thr.start()


def make_request(url):
    r = requests.get(url)
    print r.headers
    return Forecast(r.json(), url, r.headers)


def load_async(self, url, callback=None):
    try:
        self.json = json.load(urllib2.urlopen(url))
        callback(self, {'success': True, 'url': url,
                        'response': self.json})
    except urllib2.HTTPError, e:
        callback(self, {'success': False, 'url': url,
                        'response': '%s, %s' % (e.code, e.reason,)})
    except urllib2.URLError, e:
        callback(self, {'success': False, 'url': url,
                        'response': '%s, %s' % (e.code, e.reason,)})
    except Exception, e:
        callback(self, {'success': False, 'url': url, 'response': e})
