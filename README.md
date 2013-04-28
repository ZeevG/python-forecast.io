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


## License (BSD 2-clause)

Copyright (c) 2013, Ze'ev Gilovitz
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

