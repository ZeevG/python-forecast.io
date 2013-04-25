from forcastio import Forcastio

def main():
    forcast = Forcastio("YOUR API KEY")
    print forcast.loadForcast(-32.008,115.806)

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


    
if __name__ == "__main__":
    main()
