from forcastio import Forcastio

def main():
    forcast = Forcastio("ad817e0a2cb6187bca0ab7e3f648428c")
    print forcast.loadForcast(-32.008,115.806, lazy=False)

    print "===========hour========="
    byHour = forcast.getHourly()
    print byHour.summary
    
    for hourlyData in byHour.data:
        print hourlyData

    print "===========hour========="
    byHour = forcast.getHourly()
    print byHour.summary
    
    for hourlyData in byHour.data:
        print hourlyData

    print "===========daily========="
    byHour = forcast.getDaily()
    print byHour.summary
    
    for hourlyData in byHour.data:
        print hourlyData

    print "===========daily========="
    byHour = forcast.getDaily()
    print byHour.summary
    
    for hourlyData in byHour.data:
        print hourlyData


    '''temp = 0
    i = 0
    for hour in forcast.getHourly().data:
        print hour.temperature
        i = i+1
        temp = temp + hour.temperature

    print temp/i'''
    
if __name__ == "__main__":
    main()
