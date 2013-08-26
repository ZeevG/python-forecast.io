import datetime
import requests


class Forecast():
    def __init__(self, data, url, headers):
        self.url = url
        self.http_headers = headers
        self.json = data

    def update(self):
        r = requests.get(self.url)
        self.data = r.json()
        self.http_headers = r.headers

    def currently(self):
        try:
            if 'currently' not in self.json:
                url = "%s&exclude=%s" % (self.url.split('&')[0],
                      'minutely,hourly,daily,alerts,flags')

                response = requests.get(url).json()
                self.json['currently'] = response['currently']
            return ForecastioDataPoint(self.json['currently'])
        except:
            return ForecastioDataPoint()

    def minutely(self):
        try:
            if 'minutely' not in self.json:
                url = "%s&exclude=%s" % (self.url.split('&')[0],
                      'currently,hourly,daily,alerts,flags')

                response = requests.get(url).json()
                self.json['minutely'] = response['minutely']
            return ForecastioDataBlock(self.json['minutely'])
        except:
            return ForecastioDataBlock()

    def hourly(self):
        try:
            if 'hourly' not in self.json:
                url = "%s&exclude=%s" % (self.url.split('&')[0],
                      'minutely,currently,daily,alerts,flags')

                response = requests.get(url).json()
                self.json['hourly'] = response['hourly']
            return ForecastioDataBlock(self.json['hourly'])
        except:
            return ForecastioDataBlock()

    def daily(self):
        try:
            if 'daily' not in self.json:
                url = "%s&exclude=%s" % (self.url.split('&')[0],
                      'minutely,currently,hourly,alerts,flags')

                response = requests.get(url).json()
                self.json['daily'] = response['daily']
            return ForecastioDataBlock(self.json['daily'])
        except:
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
        self.windbaring = d.get('windBearing')
        self.cloudcover = d.get('cloudCover')
        self.humidity = d.get('humidity')
        self.pressure = d.get('pressure')
        self.visbility = d.get('visbility')
        self.ozone = d.get('ozone')

    def __unicode__(self):
        return '<ForecastioDataPoint instance: ' \
               '%s at %s>' % (self.summary, self.time,)

    def __str__(self):
        return unicode(self).encode('utf-8')
