from forecastio import Forecastio
import datetime


def main():
    forecast = Forecastio("YOUR API KEY")
    result = forecast.loadForecast(-31.967819, 115.87718,
                                   time=datetime.datetime.now(), units="si")
    print result

    if result['success'] is True:
        print "===========hour========="
        byHour = forecast.getHourly()
        print byHour.summary

        for hourlyDataPoint in byHour.data:
            print hourlyDataPoint

        print "===========daily========="
        byDay = forecast.getDaily()
        print byDay.summary

        for dailyDataPoint in byDay.data:
            print dailyDataPoint
    else:
        print "A problem accured communicating with the Forecast.io API"


if __name__ == "__main__":
    main()
