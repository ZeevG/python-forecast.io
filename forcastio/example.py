from forcastio import Forcastio
import datetime

def main():
    forcast = Forcastio("YOUR API KEY")
    result = forcast.loadForcast(-31.967819,115.87718, time=datetime.datetime.now(), units="si")
    print result

    if result['success'] is True:
        print "===========hour========="
        byHour = forcast.getHourly()
        print byHour.summary

        for hourlyDataPoint in byHour.data:
            print hourlyDataPoint

        print "===========daily========="
        byDay = forcast.getDaily()
        print byDay.summary

        for dailyDataPoint in byDay.data:
            print dailyDataPoint
    else:
        print "A problem accured communicating with the Forcast.io API"

    
if __name__ == "__main__":
    main()
