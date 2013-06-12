from forecastio import Forecastio
import datetime


def main():
    forecast = Forecastio("YOUR API KEY")
    result = forecast.load_forecast(-31.967819, 115.87718,
                                   time=datetime.datetime.now(), units="si")
    print result

    if result['success'] is True:
        print "===========Hourly Data========="
        by_hour = forecast.get_hourly()
        print "Hourly Summary: %s" % (by_hour.summary)

        for hourly_data_point in by_hour.data:
            print hourly_data_point

        print "===========Daily Data========="
        by_day = forecast.get_daily()
        print "Daily Summary: %s" % (by_day.summary)

        for daily_data_point in by_day.data:
            print daily_data_point
    else:
        print "A problem occurred communicating with the Forecast.io API"


if __name__ == "__main__":
    main()
