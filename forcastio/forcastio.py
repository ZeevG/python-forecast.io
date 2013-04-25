try: import simplejson as json
except ImportError: import json

import datetime

import urllib2

class ForcastioDataBlock():

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
                self.data.append(ForcastioDataPoint(datapoint))

    def __unicode__(self):
        return "<ForcastioDataBlock instance: "+self.summary +" with "+str(self.data.__len__())+" DataPoints>"



class ForcastioDataPoint():

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
            self.temperature = d['temperature']
        except:
            self.temperature = None

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

    
    def __unicode__(self):
        return "<ForcastioDataPoint instance: "+self.summary +" at "+str(self.time)+">"

    def __str__(self):
        return unicode(self).encode('utf-8')


class Forcastio():


    def __init__(self, inKey):
        self.key = inKey
        self.lat = None
        self.long = None
        self.baseURL = 'https://api.forecast.io/forecast/'
        self.json = None


    def loadForcast(self, inLat, inLong, inTime=None, lazy=True):
        self.lat = inLat
        self.long = inLong
        self.time = inTime
        self.url = self.baseURL+str(self.key)+'/'+str(self.lat)+','+str(self.long)+'?units=si'
        try:
            if lazy == True:
                baseURL = self.url + '&exclude=minutely,currently,hourly,daily,alerts,flags'
            else:
                baseURL = self.url
            self.json = json.load(urllib2.urlopen(baseURL))
            return {'success': True, 'url':baseURL, 'response':self.json}
        except urllib2.HTTPError, e:
            return {'success': False, 'url':baseURL, 'response':e.code}
        except urllib2.URLError, e:
            return {'success': False, 'url':baseURL, 'response':e.reason}
        except Exception, e:
            return {'success': False, 'url':baseURL, 'response':e}
        

    def getCurrently(self):
        try:
            if 'currently' not in self.json:
                response = json.load(urllib2.urlopen(self.url+'&exclude=minutely,hourly,daily,alerts,flags'))
                self.json['currently'] = response['currently']
            return ForcastioDataPoint(self.json['currently'])
        except:
            return ForcastioDataPoint()        

    def getMinutely(self):
        try:
            if 'minutely' not in self.json:
                response = json.load(urllib2.urlopen(self.url+'&exclude=currently,hourly,daily,alerts,flags'))
                self.json['minutely'] = response['minutely']
            return ForcastioDataBlock(self.json['minutely'])
        except:
            return ForcastioDataBlock()       

    def getHourly(self):
        try:
            if 'hourly' not in self.json:
                response = json.load(urllib2.urlopen(self.url+'&exclude=minutely,currently,daily,alerts,flags'))
                self.json['hourly'] = response['hourly']
            return ForcastioDataBlock(self.json['hourly'])
        except:
            return ForcastioDataBlock()

    def getDaily(self):
        try:
            if 'daily' not in self.json:
                response = json.load(urllib2.urlopen(self.url+'&exclude=minutely,currently,hourly,alerts,flags'))
                self.json['daily'] = response['daily']
            return ForcastioDataBlock(self.json['daily'])
        except:
            return ForcastioDataBlock()
