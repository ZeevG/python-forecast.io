try: import simplejson as json
except ImportError: import json

import datetime, time as Time, urllib2



class Forecastio():


    def __init__(self, inKey):
        self.key = inKey
        self.lat = None
        self.long = None
        self.url = None
        self.json = None


    def loadForecast(self, inLat, inLong, time=None, units="auto", lazy=False):
        """
            This function builds the request url and loads some or all of the needed json depending on lazy is True

            inLat: The latitude of the forecast
            inLong: The longitude of the forecast
            time: A datetime.datetime object representing the desired time of the forecast
            units: A string of the preferred units of measurement, "auto" id default. also us,ca,uk,si is available
            lazy: Defaults to true.  The function will only request the json data as it is needed.
                Results in more requests, but probably a faster response time (I haven't checked)
        """
        self.lat = inLat
        self.long = inLong
        self.time = time

        if self.time is None:
            self.url = 'https://api.forecast.io/forecast/'+str(self.key)+'/'+str(self.lat)+','+str(self.long)+'?units='+units
        else:
            self.url = 'https://api.forecast.io/forecast/'+str(self.key)+'/'+str(self.lat)+','+str(self.long)+','+str(int(Time.mktime(self.time.timetuple())))+'?units='+units

        if lazy == True:
                baseURL = self.url + '&exclude=minutely,currently,hourly,daily,alerts,flags'
        else:
                baseURL = self.url
        

        try:
            self.json = json.load(urllib2.urlopen(baseURL))
            return {'success': True, 'url':baseURL, 'response':self.json}
        except urllib2.HTTPError, e:
            return {'success': False, 'url':baseURL, 'response':str(e.code)+", "+e.reason}
        except urllib2.URLError, e:
            return {'success': False, 'url':baseURL, 'response':str(e.code)+", "+e.reason}
        except Exception, e:
            return {'success': False, 'url':baseURL, 'response':e}
        

    def getCurrently(self):
        try:
            if 'currently' not in self.json:
                response = json.load(urllib2.urlopen(self.url+'&exclude=minutely,hourly,daily,alerts,flags'))
                self.json['currently'] = response['currently']
            return ForecastioDataPoint(self.json['currently'])
        except:
            return ForecastioDataPoint()        

    def getMinutely(self):
        try:
            if 'minutely' not in self.json:
                response = json.load(urllib2.urlopen(self.url+'&exclude=currently,hourly,daily,alerts,flags'))
                self.json['minutely'] = response['minutely']
            return ForecastioDataBlock(self.json['minutely'])
        except:
            return ForecastioDataBlock()       

    def getHourly(self):
        try:
            if 'hourly' not in self.json:
                response = json.load(urllib2.urlopen(self.url+'&exclude=minutely,currently,daily,alerts,flags'))
                self.json['hourly'] = response['hourly']
            return ForecastioDataBlock(self.json['hourly'])
        except:
            return ForecastioDataBlock()

    def getDaily(self):
        try:
            if 'daily' not in self.json:
                response = json.load(urllib2.urlopen(self.url+'&exclude=minutely,currently,hourly,alerts,flags'))
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
        return "<ForecastioDataBlock instance: "+self.summary +" with "+str(self.data.__len__())+" DataPoints>"

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
            self.sunriseTime = datetime.datetime.fromtimestamp(int(d['sunriseTime']))
        except:
            self.sunriseTime = None

        try:
            self.sunsetTime = datetime.datetime.fromtimestamp(int(d['sunsetTime']))
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
            self.precipProbablility = d['precipProbablility']
        except:
            self.precipProbablility = None

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
        return "<ForecastioDataPoint instance: "+self.summary +" at "+str(self.time)+">"

    def __str__(self):
        return unicode(self).encode('utf-8')

