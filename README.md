## Forecast.io Wrapper

This is a wrapper for the forecast.io API.  You need an API key to use it (http://developer.forecast.io).  It also requires the urllib2 library and simplejson or json libraries, most people should have these.

The Use section covers the basics of how to use it.  I suggest also reading the source if you want to know more about how to use the wrapper or what its doing.


## Basic Use

Although you don't need to know anything about the forecast.io API to use this module, their docs are available at http://developer.forecast.io


To use the wrapper initialise a Forecastio object with your API key. Then use the load_forecast() method, passing in a lat and long.


```python
forecast = Forecastio("Your API key")
result = forecast.load_forecast(latitude,longitude)
```

Use the `forecast.getDataBlockType()` eg. `get_currently()`, `get_daily()`, `get_hourly()`, `get_minutely()` methods to load the data you are after.

These functions return a DataBlock. Except `get_currently()` which returns a DataPoint.

```python
byHour = forecast.get_hourly()
print byHour.summary
print byHour.icon
```

The .data attributes for each DataBlock is a list of DataPoint objects.

```python
for hourlyData in byHour.data:
    print hourlyData.temperature
```

## load_forecast() Options

The load_forecast() method has a few optional parameters and also returns a dict of useful data. Providing a latitude and longitude are the only required parameters.


#### Return Value
Unless called asynchronously (see below) `load_forecast()` returns a dictionary.
```python
result = forecast.load_forecast(latitude,longitude)
```
Say `load_forecast()` is called like above, `result` would be a dict with the following keys.
* result['success'] Will hold True or False depending on the response from the Forecast.io API
* result['url'] Will hold the url which is actually called by the wrapper
* result['response'] Will hold the response from the Forecast.io API.  If the request was successful this is JSON formatted data.


#### Units
You can specify the units of measurement using one of the strings "auto","us","ca","uk","si". "auto" is the default and also most likely the preferred option, it will determine the units based on the location provided. The Forecast.io docs detail exactly what the different strings mean.
```python
forecast.load_forecast(latitude,longitude, units="si")
```
#### Time
You can provide a time for the forecast either in the past or future by passing in a datetime object

```python
forecast.load_forecast(latitude,longitude, time=datetime.datetime(2013,2,1))
```

#### Lazy Execution
If you call load_forecast() with lazy=True, the data needed will be requested from the Forecast.io API as it is required. This should speed up response times.

```python
forecast.load_forecast(latitude,longitude, lazy=True)
```
At this point only a very minimal request has been made to verify the API server is up and lat, long and API key are correct.
```python
forecast.get_hourly()
```
At this point only the hourly data is requested from the Forcast.io API.

#### Asynchronous Call
A callback function accepting two parameters can also be provided which is called when the API response has been recieved. If a callback is provided, `load_forecast()` does not return anything directly and the http request is made asynchronously.

```python
def test(forecastInstance, result):
    if result['success'] == True:
        print forecastInstance.get_hourly()[0].temperature

forecast.load_forecast(latitude,longitude, callback=test)

```

Where `forecastInstance` is the Forecastio instance which made the load_forecast() call (incase you have many instances).
`result` is the dictionary which `load_forecast()` would normally return.

## License (BSD 2-clause)

Copyright (c) 2013, Ze'ev Gilovitz, Tim Heckman
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

