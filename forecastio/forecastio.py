import datetime
import requests


class Forecast():
    def __init__(self, data, url, headers):
        self.url = url
        self.HTTP_headers = headers
        self.json = data

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
               '%s with %d ForecastioDataPoints>' % (self.summary,
                                                     len(self.data),)

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
