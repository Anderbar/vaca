"""
    Classes to hold the correct vacation option
    and to output data from websites in order to send
    to frontend by the input_singleton.

"""
from website.flight_api import find_airports, find_flight_info
#from flight_api import find_airports, find_flight_info #for debug
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Vaca")

# estimated travel time for flying distance
def flying_distance(dist):
    return dist/517.5

class VacationOption: 
    def __init__(self):
        self.locName = 0
        self.cityName = 0
        self.dist = 0
        self.pricePerNight = 0
        self.travelTime = 0
        self.link = 0

    # Setters
       
    def populate(self, locName, cityName, dist, pricePerNight, travel, hotelLink):
        self.locName = locName
        self.cityName = cityName
        self.dist = dist 
        self.pricePerNight = pricePerNight
        self.travelTime = travel
        self.link = hotelLink 

    """
        Function will get data from our API that we are currently working on
    """
    def setLink(self):
        pass

    # Getters
        
    def getCityName(self):
        return self.cityName
    
    def getLocationName(self):
        return self.locName
    
    def getDistance(self):
        return self.dist
    
    def getPrice(self): 
        return self.pricePerNight
    
    def getEstimatedTravelTime(self):
        return self.travelTime
    
    
    def getLink(self):
        return self.link
    
        
    def getAll(self):
        return [self.locName, self.cityName, self.dist, self.pricePerNight, self.travelTime, self.link]
        # hotel link : 5

    


# this is a child class for parent, still being worked on
class VacationOptionWithFlight(VacationOption):
    def __init__(self) -> None:
        self.locName = 0
        self.originalName = 0
        self.cityName = 0
        self.startDate = 0
        self.endDate = 0
        self.travelers = 1
        self.dist = 0
        self.pricePerNight = 0
        self.travelTime = 0
        self.link = 0
        self.flightLink = 0

        self.startAirport = 0
        self.endAirport = 0
        self.flightCost = 0
        self.flightName = 0
        self.airlineName = 0

        self.returnName = 0
        self.returnAirline = 0


    # Setters
    
    def populateFlightInfo(self, locName, cityName, originalName, dist, pricePerNight, startDate, endDate, hotelLink):
        self.locName = locName
        self.cityName = cityName
        self.originalName = originalName
        self.dist = dist
        self.pricePerNight = pricePerNight
        self.startDate = startDate
        self.endDate = endDate
        self.travelTime = flying_distance(self.dist)
        self.startAirport = find_airports(self.originalName)
        self.endAirport = find_airports(self.cityName)
        self.link = hotelLink
        

    """
        Functions will get data from our API that we are currently working on
    """
    def setLink(self):
        return super().setLink()

    def collectAirFlightData(self):


        if self.dist == 0:
            return 
        else:

            check = find_flight_info(self.startAirport["name"], self.endAirport["name"], self.travelers, self.startDate, self.endDate)
            #print(check)
            self.flightCost = check["price"]
            #self.startAirport = check["outbound"][0]["origin"]
            #self.endAirport = check["outbound"][0]["dest"]
            self.airlineName = check["outbound"][0]["airline"]
            self.flightName = check["outbound"][0]["flight"]

            self.returnName = check["return"][0]["flight"]
            self.returnAirline = check["return"][0]["airline"]
            
            self.flightLink = check["link0"]
            #print(check["price"], check["outbound"][0]["origin"], check["outbound"][0]["dest"], check["outbound"][0]["airline"], check["outbound"][0]["flight"])




    # Getters

    def getCityName(self):
        return super().getCityName()

    def getDistance(self):
        return super().getDistance()

    def getLocationName(self):
        return super().getLocationName()

    def getPrice(self):
        return super().getPrice()

    def getLink(self):
        return super().getLink()

    def airportSameCheck(self):
        return self.startAirport["name"] == self.endAirport["name"]

    def getFlightCost(self):
        return self.flightCost

    def getAllWithFlight(self):
        return [self.locName, self.cityName, round(self.dist), self.pricePerNight, round(self.travelTime, 2), self.airlineName, self.startAirport["name"], self.endAirport["name"], self.flightName, self.flightLink, self.flightCost, self.returnName, self.returnAirline, self.link]
        # flight link : 9
        # hotel link : 13

"""
if __name__ == '__main__':

    cityTxt = "New York NY"
    endTxt = "Troy NY"

    startLocInfo = geolocator.geocode(cityTxt)
    startCords = (startLocInfo.latitude, startLocInfo.longitude)

    currLocInfo = geolocator.geocode(endTxt)
    currCords = (currLocInfo.latitude, currLocInfo.longitude)

    currDistance = geopy.distance.geodesic(startCords, currCords).miles


    
    

    airport1 = find_airports(cityTxt)
    airport2 = find_airports(endTxt)

    travelers = "1"
    dep_date = "2022-08-06"
    arr_date = "2022-08-08"

    flightOption = VacationOptionWithFlight()
    flightOption.populateFlightInfo("Mi Casa", endTxt, cityTxt, round(currDistance), 10, dep_date, arr_date)

    flightOption.collectAirFlightData()
    print(flightOption.getAllWithFlight())


"""   