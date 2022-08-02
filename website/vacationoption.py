"""
    Classes to hold the correct vacation option
    and to output data from websites in order to send
    to frontend by the input_singleton.

"""

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
       
    def populate(self, locName, cityName, dist, pricePerNight, travel):
        self.locName = locName
        self.cityName = cityName
        self.dist = dist 
        self.pricePerNight = pricePerNight
        self.travelTime = travel 

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
        return [self.locName, self.cityName, self.dist, self.pricePerNight, self.travelTime]

    


# this is a child class for parent, still being worked on
class VacationOptionWithFlight(VacationOption):
    def __init__(self) -> None:
        def __init__(self):
            self.locName = 0
            self.cityName = 0
            self.dist = 0
            self.pricePerNight = 0
            self.travelTime = 0
            self.link = 0
            self.flightLink = 0
            self.startAirport = 0
            self.endAirport = 0
            self.timeOfFlight = 0

    # Setters
    
    def populate(self, locName, cityName, dist, pricePerNight):
        return super().populate(locName, cityName, dist, pricePerNight, 0)

    """
        Functions will get data from our API that we are currently working on
    """
    def setLink(self):
        return super().setLink()

    def collectAirFlightData(self):
        pass

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
