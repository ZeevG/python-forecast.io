## Forcast.io Wrapper

This is a wrapper for the forcast.io API.  You need an API key to use it (http://developer.forecast.io).  It also requires the liburl2 library and simplejson or json libraries, most people shouldhave these.


## Diclaimer
This is only a very initial version so not all data is available, there are no code comments yet (alought is all very simple), and it may be a bit buggy.  The Use section explains the basics of how to use it.  I suggest also reading the source if you want to know more about how to use the wrapper or what its doing.


## Use

Although you don't need to know anything about the forcast.io API to use this module, their docs are available at http://developer.forecast.io


To use the wrapper initialise a Forcastio object with your API key. Then use the loadForcast() method, passing in a lat and long.


```python
forcast = Forcastio("Your API key")
result = forcast.loadForcast(latitude,longitude)
```

Use the `forcast.getDataBlockType()` eg. `getCurrently()`, `getDaily()`, `getHourly()`, `getMinutely()` methods to load the data you are after.

These functions return a DataBlock. Except `getCurrently()` which returns a DataPoint.

Unless you call loadForcast() with lazy=False, these methods are lazy.  They will retrieve the needed data when they are first called.


```python
byHour = forcast.getHourly()
print byHour.summary
print byHour.icon
```

The .data attributes for each DataBlock is a list of DataPoint objects.

```python
for hourlyData in byHour.data:
    print hourlyData.temperature
```

