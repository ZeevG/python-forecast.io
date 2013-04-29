## orecast.io Wrapper

This is a wrapper for the forecast.io API.  You need an API key to use it (http://developer.forecast.io).  It also requires the liburl2 library and simplejson or json libraries, most people shouldhave these.


## Diclaimer
This is only a very initial version so not all data is available, there are no code comments yet (alought is all very simple), and it may be a bit buggy.  The Use section explains the basics of how to use it.  I suggest also reading the source if you want to know more about how to use the wrapper or what its doing.


## Use

Although you don't need to know anything about the forecast.io API to use this module, their docs are available at http://developer.forecast.io


To use the wrapper initialise a Forecastio object with your API key. Then use the loadForecast() method, passing in a lat and long.


```python
forecast = Forecastio("Your API key")
result = forecast.loadForecast(latitude,longitude)
```

Use the `forecast.getDataBlockType()` eg. `getCurrently()`, `getDaily()`, `getHourly()`, `getMinutely()` methods to load the data you are after.

These functions return a DataBlock. Except `getCurrently()` which returns a DataPoint.

Unless you call loadForecast() with lazy=False, these methods are lazy.  They will retrieve the needed data when they are first called.


```python
byHour = forecast.getHourly()
print byHour.summary
print byHour.icon
```

The .data attributes for each DataBlock is a list of DataPoint objects.

```python
for hourlyData in byHour.data:
    print hourlyData.temperature
```

