

class VacationOption: 
    def __init__(self):
        self.locName = 0
        self.cityName = 0
        self.dist = 0
        self.pricePerNight = 0
        self.travelTime = 0
#       self.link = 0
       
    def populate(self, locName, cityName, dist, pricePerNight, travel):
        self.locName = locName
        self.cityName = cityName
        self.dist = dist 
        self.pricePerNight = pricePerNight
        self.travelTime = travel 
        
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
    
    '''
    def getLink(self):
    return self.link
    '''
        
    def getAll(self):
        return [self.locName, self.cityName, self.dist, self.pricePerNight, self.travelTime]


# this is a child class for parent, still being worked on
class VacationOptionWithFlight:
    def __init__(self) -> None:
        pass
