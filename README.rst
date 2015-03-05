*******************
Forecast.io Wrapper
*******************

.. image:: https://travis-ci.org/ZeevG/python-forecast.io.svg?branch=master

This is a wrapper for the forecast.io API. It allows you to get the weather for any location, now, in the past, or future.

The Basic Use section covers enough to get you going. I suggest also reading the source if you want to know more about how to use the wrapper or what its doing (it's very simple).


Installation
############
You should use pip to install python-forecastio.

* To install pip install python-forecastio
* To remove pip uninstall python-forecastio

Simple!

Requirements
############

- You need an API key to use it (http://developer.forecast.io). Don't worry a key is free.


Basic Use
#########

Although you don't need to know anything about the forecast.io API to use this module, their docs are available at http://developer.forecast.io

To use the wrapper:

.. code-block:: python

	import forecastio

	api_key = "YOUR API KEY"
	lat = -31.967819
	lng = 115.87718

	forecast = forecastio.load_forecast(api_key, lat, lng)
	...

The ``load_forecast()`` method has a few optional parameters. Providing your API key, a latitude and longitude are the only required parameters.

Use the ``forecast.DataBlockType()`` eg. ``currently()``, ``daily()``, ``hourly()``, ``minutely()`` methods to load the data you are after.

These methods return a DataBlock. Except ``currently()`` which returns a DataPoint.

.. code-block:: python

	byHour = forecast.hourly()
	print byHour.summary
	print byHour.icon


The .data attributes for each DataBlock is a list of DataPoint objects. This is where all the good data is :)

.. code-block:: python

	for hourlyData in byHour.data:
		print hourlyData.temperature



Advanced
########

*function* forecastio.load_forecast(key, latitude, longitude)
---------------------------------------------------

This makes an API request and returns a **Forecast** object (see below).

Parameters:
	- **key** - Your API key from https://developer.forecast.io/
	- **latitude** - The latitude of the location for the forecast
	- **longitude** - The longitude of the location for the forecast
	- **time** - (optional) A datetime object for the forecast either in the past or future
	- **units** - (optional) A string of the preferred units of measurement, "auto" is the default. "us","ca","uk","si" are also available. See the API Docs https://developer.forecast.io/docs/v2 for exactly what each unit means.
	- **lazy** - (optional) Defaults to `false`.  If `true` the function will request the json data as it is needed. Results in more requests, but maybe a faster response time.
	- **callback** - (optional) Pass a function to be used as a callback. If used, load_forecast() will use an asynchronous HTTP call and **will not return the forecast object directly**, instead it will be passed to the callback function. Make sure it can accept it.

----------------------------------------------------


*function* forecastio.manual(url)
----------------------------------------------------
This function allows manual creation of the URL for the Forecast.io API request.  This method won't be required often but can be used to take advantage of new or beta features of the API which this wrapper does not support yet. Returns a **Forecast** object (see below).

Parameters:
        - **url** - The URL which the wrapper will attempt build a forecast from.
    	- **callback** - (optional) Pass a function to be used as a callback. If used, an asynchronous HTTP call will be used and ``forecastio.manual`` **will not return the forecast object directly**, instead it will be passed to the callback function. Make sure it can accept it.

----------------------------------------------------


*class* forecastio.models.Forecast
------------------------------------

The **Forecast** object, it contains both weather data and the HTTP response from forecast.io

**Attributes**
	- **response**
		- The Response object returned from requests request.get() method. See https://requests.readthedocs.org/en/latest/api/#requests.Response
	- **http_headers**
		- A dictionary of response headers. 'X-Forecast-API-Calls' might be of interest, it contains the number of API calls made by the given API key for today.
	- **json**
		- A dictionary containing the json data returned from the API call.

**Methods**
	- **currently()**
		- Returns a ForecastioDataPoint object
	- **minutely()**
		- Returns a ForecastioDataBlock object
	- **hourly()**
		- Returns a ForecastioDataBlock object
	- **daily()**
		- Returns a ForecastioDataBlock object
	- **update()**
		- Refreshes the forecast data by making a new request.

----------------------------------------------------


*class* forecastio.models.ForecastioDataBlock
---------------------------------------------

Contains data about a forecast over time.

**Attributes** *(descriptions taken from the forecast.io website)*
	- **summary**
		- A human-readable text summary of this data block.
	- **icon**
		- A machine-readable text summary of this data block.
	- **data**
		- An array of **ForecastioDataPoint** objects (see below), ordered by time, which together describe the weather conditions at the requested location over time.

----------------------------------------------------


*class* forecastio.models.ForecastioDataPoint
---------------------------------------------

Contains data about a forecast at a particular time.

Data points have many attributes, but **not all of them are always available**. Some commonly used ones are:

**Attributes** *(descriptions taken from the forecast.io website)*
	-	**summary**
		- A human-readable text summary of this data block.
	-	**icon**
		- A machine-readable text summary of this data block.
	-	**time**
		- The time at which this data point occurs.
	-	**temperature**
		- (not defined on daily data points): A numerical value representing the temperature at the given time.
	-	**precipProbability**
		- A numerical value between 0 and 1 (inclusive) representing the probability of precipitation occurring at the given time.

For a full list of ForecastioDataPoint attributes and attribute descriptions, take a look at the forecast.io data point documentation (https://developer.forecast.io/docs/v2#data-points)
