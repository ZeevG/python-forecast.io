## Forecast.io Wrapper

This is a wrapper for the forecast.io API.  You need an API key to use it (http://developer.forecast.io).  It also requires the requests library (http://docs.python-requests.org) which you can install using `pip install requests`

The Use section covers the basics of how to use it.  I suggest also reading the source if you want to know more about how to use the wrapper or what its doing.


## Recent Changes

* python-requests is now used for requests. This adds the following benifits:
	* Gzip compression
	* HTTPS is used

* Updates to the way load_forecast is used. This should make it easier to keep track of the state of your Forecast objects.


## Basic Use

Although you don't need to know anything about the forecast.io API to use this module, their docs are available at http://developer.forecast.io


To use the wrapper import Forecastio as in the example script. Then call the function forecastio.load_forecast(), passing it your API key, a lat and a long. This returns a Forecast object.


```python
import forecastio

api_key = "YOUR API KEY"
lat = -31.967819
lng = 115.87718

forecast = forecastio.load_forecast(api_key, lat, lng)
```

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

## load_forecast() Options

The load_forecast() method has a few optional parameters. Providing your API key and a latitude and longitude are the only required parameters.


#### Units
You can specify the units of measurement using one of the strings "auto","us","ca","uk","si". "auto" is the default and also most likely the preferred option, it will determine the units based on the location provided. The Forecast.io docs detail exactly what the different strings mean.
```python
forecast.load_forecast(latitude,longitude, units="si")
```
#### Time
You can provide a time for the forecast either in the past or future by passing in a datetime object

```python
forecast.load_forecast(api_key, latitude, longitude, time=datetime.datetime(2013,2,1))
```

#### Lazy Execution
If you call load_forecast() with lazy=True, the data needed will be requested from the Forecast.io API as it is required. This should speed up response times.

```python
forecast.load_forecast(api_key, latitude, longitude, lazy=True)
```
At this point only a very minimal request has been made to verify the API server is up and lat, long and API key are correct.
```python
forecast.hourly()
```
At this point only the hourly data is requested from the Forcast.io API.

#### Asynchronous Call
A callback function can also be provided which is called when the API response has been recieved. If a callback is provided, `load_forecast()` does not return anything directly and the http request is made asynchronously.

```python
def test(forecast):
    print forecast.hourly().data[0].temperature

forecastio.load_forecast(api_key, lat, lng, callback=test)

```

Where `forecast` is the Forecast instance which is normally returned from `load_forecast()`

#### Update Forecast Data
Forecast objects have an `update()` method which you can use to refresh the forecast data.

## License (BSD 2-clause)

Copyright (c) 2013, Ze'ev Gilovitz and contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

