import datetime
import requests


class Forecast():
    def __init__(self, data, response, headers):
        self.response = response
        self.http_headers = headers
        self.json = data

    def update(self):
        r = requests.get(self.response.url)
        self.json = r.json()
        self.response = r

    def currently(self):
        return self._forcastio_data('currently')

    def minutely(self):
        return self._forcastio_data('minutely')

    def hourly(self):
        return self._forcastio_data('hourly')

    def daily(self):
        return self._forcastio_data('daily')
        
    def offset(self):
        return self.json['offset']

    def _forcastio_data(self, key):
        keys = ['minutely', 'currently', 'hourly', 'daily']
        try:
            if key not in self.json:
                keys.remove(key)
                url = "%s&exclude=%s%s" % (self.response.url.split('&')[0],
                      ','.join(keys), ',alerts,flags')

                response = requests.get(url).json()
                self.json[key] = response[key]

            if key == 'currently':
                return ForecastioDataPoint(self.json[key])
            else:
                return ForecastioDataBlock(self.json[key])
        except:
            if key == 'currently':
                return ForecastioDataPoint()
            else:
                return ForecastioDataBlock()

class ForecastioDataBlock():
    def __init__(self, d=None):
        d = d or {}
        self.summary = d.get('summary')
        self.icon = d.get('icon')

        self.data = [ForecastioDataPoint(datapoint) 
                     for datapoint in d.get('data', [])]

    def __unicode__(self):
        return '<ForecastioDataBlock instance: ' \
               '%s with %d ForecastioDataPoints>' % (self.summary,
                                                     len(self.data),)

    def __str__(self):
        return unicode(self).encode('utf-8')


class ForecastioDataPoint():
    def __init__(self, d=None):
        d = d or {}

        try:
            self.time = datetime.datetime.fromtimestamp(int(d['time']))
        except:
            self.time = None

        self.utime = d.get('time')
        self.icon = d.get('icon')
        self.summary = d.get('summary')

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

        self.precipIntensity = d.get('precipIntensity')
        self.precipIntensityMax = d.get('precipIntensityMax')
        self.precipIntensityMaxTime = d.get('precipIntensityMaxTime')
        self.precipProbability = d.get('precipProbability')
        self.precipType = d.get('precipType')
        self.precipAccumulation = d.get('precipAccumulation')
        self.temperature = d.get('temperature')
        self.temperatureMin = d.get('temperatureMin')
        self.temperatureMinTime = d.get('temperatureMinTime')
        self.temperatureMax = d.get('temperatureMax')
        self.temperatureMaxTime = d.get('temperatureMaxTime')
        self.dewPoint = d.get('dewPoint')
        self.windspeed = d.get('windSpeed')
        self.windbearing = d.get('windBearing')
        self.cloudcover = d.get('cloudCover')
        self.humidity = d.get('humidity')
        self.pressure = d.get('pressure')
        self.visibility = d.get('visibility')
        self.ozone = d.get('ozone')

    def __unicode__(self):
        return '<ForecastioDataPoint instance: ' \
               '%s at %s>' % (self.summary, self.time,)

    def __str__(self):
        return unicode(self).encode('utf-8')
