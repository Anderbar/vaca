import csv
import geopy.distance
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Vaca")

class Input:
    def __init__(self):
        self.budget = 0
        self.startDate = 0
        self.endDate = 0
        self.startLoc = 0
        self.rating = 0
        self.distance_preference = 0
        self.travelpreference = 0
        self.iter = 0
        self.startLocInfo = 0
        self.latlongLoc = 0


    def newInput(self, budget, startDate, endDate, startLoc, rating, distance_preference, travel_preference):
        self.budget = budget
        self.startDate = startDate
        self.endDate = endDate
        self.startLoc = startLoc
        self.rating = rating
        self.distance_preference = distance_preference
        self.travelpreference = travel_preference
        self.startLocInfo = geolocator.geocode(self.startLoc)
        self.latlongLoc = (self.startLocInfo.latitude, self.startLocInfo.longitude)

    def getLocation(self):
        return self.startLoc

    def getStartDate(self):
        return self.startDate

    def getEndDate(self):
        return self.endDate

    def getRating(self):
        return self.rating

    def getPrice(self):
        return self.budget

    def getVacationOption(self):
        count = 0
        with open('testdata.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)

            for row in reader:
                # pass through to newer entries of database
                if count < iter:
                    count += 1
                    continue

                # budget check
                if self.budget >= row[1]:
                    # rating check
                    if row[2] in self.rating:
                      # distance check
                      
                      
                      currLocInfo = geolocator.geocode(row[3])
                      currCords = (currLocInfo.latitude, currLocInfo.longitude)
                      currDistance = geopy.distance.geodesic(self.latlongLoc, currCords).miles

                      # no distance preference
                      if self.distance_preference != 0:
                        pass
                    
                      # distance preference
                      else:
                        if self.distance_preference <= currDistance:
                            pass




