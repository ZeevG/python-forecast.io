## Forecast.io Wrapper

This is a wrapper for the forecast.io API. It allows you to get the weather for any location, now, in the past, or future.

I was originally looking for a good python weather API to use in another project. When I struggled to find anything I liked, I decided to write this one.

The Basic Use section covers enough to get you going. I suggest also reading the source if you want to know more about how to use the wrapper or what its doing (it's very simple).

## Recent Changes

* python-requests is now used for requests. Among other things, this adds the following benefits:
	* Gzip compression

	* HTTPS is used

* Updates to the way load_forecast is used. This should make it easier to keep track of the state of your Forecast objects.


## Requirements

* You need an API key to use it (http://developer.forecast.io). Don't worry a key is free.
* Also, the requests library (http://docs.python-requests.org) which you can install using `pip install requests`


## Basic Use

Although you don't need to know anything about the forecast.io API to use this module, their docs are available at http://developer.forecast.io

To use the wrapper `import forecastio` as in the example script. Then call the function `forecastio.load_forecast()` You can use the function like this.

```python
import forecastio

api_key = "YOUR API KEY"
lat = -31.967819
lng = 115.87718

forecast = forecastio.load_forecast(api_key, lat, lng)
```

The load_forecast() method has a few optional parameters. Providing your API key and a latitude and longitude are the only required parameters.

Use the `forecast.DataBlockType()` eg. `currently()`, `daily()`, `hourly()`, `minutely()` methods to load the data you are after.

These functions return a DataBlock. Except `currently()` which returns a DataPoint.

```python
byHour = forecast.hourly()
print byHour.summary
print byHour.icon
```

The .data attributes for each DataBlock is a list of DataPoint objects.

```python
for hourlyData in byHour.data:
    print hourlyData.temperature
```


## Advanced

####forecastio.load_forecast(key, latitude, longitude)

This makes an API request and returns a **Forecast** object (see below).

Parameters:
  * **key** - Your API key from https://developer.forecast.io/
  * **latitude** - The latitude of the location for the forecast
  * **longitude** - The longitude of the location for the forecast
  * **time** - (optional) A datetime object for the forecast either in the past or future
  * **units** - (optional) A string of the preferred units of measurement, "auto" is the default. "us","ca","uk","si" are also available. See the API Docs https://developer.forecast.io/docs/v2 for exactly what each unit means.
  * **lazy** - (optional) Defaults to `false`.  If `true` the function will request the json data as it is needed. Results in more requests, but maybe a faster response time.
  * **callback** - (optional) Pass a function to be used as a callback. If used, load_forecast() will use an asynchronous HTTP call and **will not return the forecast object directly**, instead it will be passed to the callback function. Make sure it can accept it.

---

####*class* forecastio.models.Forecast

The **Forecast** object, it contains both weather data and the HTTP response from forecast.io

**Attributes**
  + **response**
    + The Response object returned from requests request.get() method. See https://requests.readthedocs.org/en/latest/api/#requests.Response
  + **http_headers**
    + A dictionary of response headers. 'X-Forecast-API-Calls' might be of interest, it contains the number of API calls made by the given API key for today.
  + **json**
    + A dictionary containing the json data returned from the API call.

**Methods**
  + **currently()**
    + Returns a ForecastioDataPoint object
  + **minutely()**
    + Returns a ForecastioDataBlock object
  + **hourly()**
    + Returns a ForecastioDataBlock object
  + **daily()**
    + Returns a ForecastioDataBlock object
  + **update()**
  	+ Refreshes the forecast data by making a new request.

---

####*class* forecastio.models.ForecastioDataBlock
Contains data about a forecast over time.

**Attributes** *(descriptions taken from the forecast.io website)*
  + **summary**
    + A human-readable text summary of this data block.
  + **icon**
    + A machine-readable text summary of this data block.
  + **data**
    + An array of **ForecastioDataPoint** objects (see below), ordered by time, which together describe the weather conditions at the requested location over time.

---

####*class* forecastio.models.ForecastioDataPoint
Contains data about a forecast at a particular time.

Data points have many attributes, but **not all of them are always available**. Some commonly used ones are:

**Attributes** *(descriptions taken from the forecast.io website)*
  + **summary**
    + A human-readable text summary of this data block.
  + **icon**
    + A machine-readable text summary of this data block.
  + **time**
    + The time at which this data point occurs.
  + **temperature**
    + (not defined on daily data points): A numerical value representing the temperature at the given time.
  + **precipProbability**
    + A numerical value between 0 and 1 (inclusive) representing the probability of precipitation occurring at the given time.

 For a full list of ForecastioDataPoint attributes and attribute descriptions, take a look at the forecast.io data point documentation (https://developer.forecast.io/docs/v2#data-points)


## License (BSD 2-clause)

Copyright (c) 2013, Ze'ev Gilovitz and contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
