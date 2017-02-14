import forecast

API_KEY = "YOUR_KEY"


def main(forecast):

    print forecast.hourly().data[0].temperature
    print "===========Hourly Data========="
    by_hour = forecast.hourly()
    print "Hourly Summary: %s" % (by_hour.summary)

    for hourly_data_point in by_hour.data:
        print hourly_data_point

    print "===========Daily Data========="
    by_day = forecast.daily()
    print "Daily Summary: %s" % (by_day.summary)

    for daily_data_point in by_day.data:
        print daily_data_point


def data_with_lat_lng():
    lat = -31.967819
    lng = 115.87718
    print("Forecast with Lat/Lng Specified")
    return forecast.load(API_KEY, lat, lng)


def data_with_address():
    address = 'New York City, NY'
    print("A forecast generated with geocoding.")
    return forecast.geocode(API_KEY, address=address)


if __name__ == "__main__":
    main(data_with_lat_lng())
    main(data_with_address())
