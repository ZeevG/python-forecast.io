try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        print('It appears you are running an older version of Python, '
              'please install simplejson from the cheese shop.')
        quit()
from multiprocessing import Pool
import datetime
import time as Time
import urllib2
import threading
import Queue
import warnings


class Forecastio():

    def __init__(self, inKey):
        self.key = inKey
        self.lat = None
        self.long = None
        self.url = None
        self.json = None

    def loadForecast(self, inLat, inLong, time=None, units="auto", lazy=False,
                     callback=None):
        """
        Deprecated for PEP 8 compliance
        """
        params = locals()
        del params['self']
        warnings.simplefilter('default')
        warnings.warn('"loadForecast()" deprecated, please use '
                      '"load_forecast()"',
                      DeprecationWarning)
        return self.load_forecast(**params)

    def load_forecast(self, inLat, inLong, time=None, units="auto", lazy=False,
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

        self.lat = inLat
        self.long = inLong
        self.time = time

        if self.time is None:
            self.url = 'https://api.forecast.io/forecast/%s/%s,%s' \
                       '?units=%s' % (self.key, self.lat, self.long, units,)
        else:
            url_time = str(int(Time.mktime(self.time.timetuple())))
            self.url = 'https://api.forecast.io/forecast/%s/%s,%s,%s' \
                       '?units=%s' % (self.key, self.lat, self.long, url_time,
                                      units,)

        if lazy is True:
            baseURL = "%s&exclude=%s" % (self.url,
                                         'minutely,currently,hourly,'
                                         'daily,alerts,flags')
        else:
            baseURL = self.url

        if callback is None:
            try:
                self.json = json.load(urllib2.urlopen(baseURL))
                return {'success': True, 'url': baseURL, 'response': self.json}
            except urllib2.HTTPError, e:
                return {'success': False, 'url': baseURL,
                        'response': '%s, %s' % (e.code, e.reason,)}
            except urllib2.URLError, e:
                return {'success': False, 'url': baseURL,
                        'response': '%s, %s' % (e.code, e.reason,)}
            except Exception, e:
                return {'success': False, 'url': baseURL, 'response': e}

        else:
            thr = threading.Thread(target=self.load_async, args=(baseURL,),
                                   kwargs={'callback': callback})
            thr.start()

    def loadAsync(self, url, callback=None):
        """
        Deprecated for PEP 8 compliance
        """
        params = locals()
        del params['self']
        warnings.simplefilter('default')
        warnings.warn('"loadAsync()" deprecated, please use "load_async()"',
                      DeprecationWarning)
        self.load_async(**params)

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

    def getCurrently(self):
        """
        Deprecated for PEP 8 compliance
        """
        params = locals()
        del params['self']
        warnings.simplefilter('default')
        warnings.warn('"getCurrently()" deprecated, please use '
                      '"get_currently()"',
                      DeprecationWarning)
        return self.get_currently(**params)

    def get_currently(self):
        try:
            if 'currently' not in self.json:
                url = "%s&exclude=%s" % (self.url, 'minutely,hourly,daily,'
                                                   'alerts,flags',)
                response = json.load(urllib2.urlopen(url))
                self.json['currently'] = response['currently']
            return ForecastioDataPoint(self.json['currently'])
        except:
            return ForecastioDataPoint()

    def getMinutely(self):
        """
        Deprecated for PEP 8 compliance
        """
        params = locals()
        del params['self']
        warnings.simplefilter('default')
        warnings.warn('"getMinutely()" deprecated, please use '
                      '"get_minutely()"',
                      DeprecationWarning)
        return self.get_minutely(**params)

    def get_minutely(self):
        try:
            if 'minutely' not in self.json:
                url = "%s&exclude=%s" % (self.url, 'currently,hourly,daily,'
                                                   'alerts,flags',)
                response = json.load(urllib2.urlopen(url))
                self.json['minutely'] = response['minutely']
            return ForecastioDataBlock(self.json['minutely'])
        except:
            return ForecastioDataBlock()

    def getHourly(self):
        """
        Deprecated for PEP 8 compliance
        """
        params = locals()
        del params['self']
        warnings.simplefilter('default')
        warnings.warn('"getHourly()" deprecated, please use "get_hourly()"',
                      DeprecationWarning)
        return self.get_hourly(**params)

    def get_hourly(self):
        try:
            if 'hourly' not in self.json:
                url = "%s&exclude=%s" % (self.url, 'minutely,currently,daily,'
                                                   'alerts,flags')
                response = json.load(urllib2.urlopen(url))
                self.json['hourly'] = response['hourly']
            return ForecastioDataBlock(self.json['hourly'])
        except:
            return ForecastioDataBlock()

    def getDaily(self):
        """
        Deprecated for PEP 8 compliance
        """
        params = locals()
        del params['self']
        warnings.simplefilter('default')
        warnings.warn('"getDaily()" deprecated, please use "get_daily()"',
                      DeprecationWarning)
        return self.get_daily(**params)

    def get_daily(self):
        try:
            if 'daily' not in self.json:
                url = "%s&exclude=%s" % (self.url, 'minutely,currently,hourly,'
                                                   'alerts,flags')
                response = json.load(urllib2.urlopen(url))
                self.json['daily'] = response['daily']
            return ForecastioDataBlock(self.json['daily'])
        except:
            return ForecastioDataBlock()


class ForecastioDataBlock():

    def __init__(self, d=None):
        try:
            self.summary = d['summary']
        except:
            self.summary = None
        try:
            self.icon = d['icon']
        except:
            self.icon = None

        self.data = []

        if d is not None:
            for datapoint in d['data']:
                self.data.append(ForecastioDataPoint(datapoint))

    def __unicode__(self):
        return '<ForecastioDataBlock instance: ' \
               '%s with %d DataPoints>' % (self.summary, len(self.data),)

    def __str__(self):
        return unicode(self).encode('utf-8')


class ForecastioDataPoint():

    def __init__(self, d=None):

        try:
            self.time = datetime.datetime.fromtimestamp(int(d['time']))
        except:
            self.time = None

        try:
            self.icon = d['icon']
        except:
            self.icon = None

        try:
            self.summary = d['summary']
        except:
            self.summary = None

        try:
            sr_time = int(d['sunriseTime'])
            self.sunriseTime = datetime.datetime.fromtimestamp(sr_time)
        except:
            self.sunriseTime = None

        try:
            ss_time = int(d['sunsetTime'])
            self.sunsetTime = datetime.datetime.fromtimestamp(ss_time)
        except:
            self.sunsetTime = None

        try:
            self.precipIntensity = d['precipIntensity']
        except:
            self.precipIntensity = None

        try:
            self.precipIntensityMax = d['precipIntensityMax']
        except:
            self.precipIntensityMax = None

        try:
            self.precipIntensityMaxTime = d['precipIntensityMaxTime']
        except:
            self.precipIntensityMaxTime = None

        try:
            self.precipProbability = d['precipProbability']
        except:
            self.precipProbability = None

        try:
            self.precipType = d['precipType']
        except:
            self.precipType = None

        try:
            self.precipAccumulation = d['precipAccumulation']
        except:
            self.precipAccumulation = None

        try:
            self.temperature = d['temperature']
        except:
            self.temperature = None

        try:
            self.temperatureMin = d['temperatureMin']
        except:
            self.temperatureMin = None

        try:
            self.temperatureMinTime = d['temperatureMinTime']
        except:
            self.temperatureMinTime = None

        try:
            self.temperatureMax = d['temperatureMax']
        except:
            self.temperatureMax = None

        try:
            self.temperatureMaxTime = d['temperatureMaxTime']
        except:
            self.temperatureMaxTime = None

        try:
            self.dewPoint = d['dewPoint']
        except:
            self.dewPoint = None

        try:
            self.windspeed = d['windSpeed']
        except:
            self.windspeed = None

        try:
            self.windbaring = d['windBearing']
        except:
            self.windbaring = None

        try:
            self.cloudcover = d['cloudCover']
        except:
            self.cloudcover = None

        try:
            self.humidity = d['humidity']
        except:
            self.humidity = None

        try:
            self.pressure = d['pressure']
        except:
            self.pressure = None

        try:
            self.visbility = d['visbility']
        except:
            self.visbility = None

        try:
            self.ozone = d['ozone']
        except:
            self.ozone = None

    def __unicode__(self):
        return '<ForecastioDataPoint instance: ' \
               '%s at %s>' % (self.summary, self.time,)

    def __str__(self):
        return unicode(self).encode('utf-8')
