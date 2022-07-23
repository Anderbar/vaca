import csv
import geopy.distance
from geopy.geocoders import Nominatim
from website.vacationoption import VacationOption

geolocator = Nominatim(user_agent="Vaca")

def driving_distance(dist):
    return dist/70.4

def flying_distance(dist):
    return dist/517.5


class Input:
    def __init__(self):
        self.budget = 0
        self.startDate = 0
        self.endDate = 0
        self.startLoc = 0
        self.rating = 0
        self.distance_preference = 0
        self.travelpreference = 0
        #int to determine how many times we have found an option
        self.iter = 0
        self.startLocInfo = 0
        self.latlongLoc = 0
        #bool to determine if we have found an option
        self.findOption = False


    def newInput(self, budget, startDate, endDate, startLoc, rating, distancepreference, travelpreference):
        self.budget = int(budget)
        self.startDate = startDate
        self.endDate = endDate
        self.startLoc = startLoc
        self.rating = rating
        self.distancepreference = int(distancepreference)
        self.travelpreference = travelpreference
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

    def getStuffTest(self):
        return ["Marriot", "NYC", "200", "99", "2.5"]

    def getVacationOption(self):
        print("self.iter:", self.iter)
        count = self.iter
        resumeCount = 0
        reachedOption = False
        with open('testdata.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            #print("length of reader:", len(reader))

            for row in reader:
                # pass through to newer entries of database
                if resumeCount < self.iter:
                    resumeCount += 1
                    continue

                # budget check
                if self.budget >= int(row[1]):

                    # rating check
                    if len(self.rating) == 0:
                        # distance check
                        currLocInfo = geolocator.geocode(row[3])
                        currCords = (currLocInfo.latitude, currLocInfo.longitude)
                        currDistance = geopy.distance.geodesic(self.latlongLoc, currCords).miles

                        # no distance preference
                        if self.distancepreference != 0:
                            if self.travelpreference == 'Car':
                                #print("Found option 1") #debug

                                # return for frontend
                                opt = VacationOption()
                                opt.populate(row[0], row[3], currDistance, row[1], driving_distance(currDistance))
                                # update vars during loop
                                count += 1
                                self.iter = count
                                self.findOption = True
                                reachedOption = True
                                break

                            else:
                                pass
                        # distance preference
                        else:
                            if self.distancepreference <= currDistance:
                                if self.travelpreference == 'Car':
                                    #print("Found option 2") #debug
                                    opt = VacationOption()
                                    opt.populate(row[0], row[3], currDistance, row[1], driving_distance(currDistance))
                                    count += 1
                                    self.iter = count
                                    self.findOption = True
                                    reachedOption = True
                                    break
                                else:
                                    pass
        
                    else:

                        if row[2] in self.rating:
                            # distance check
                            currLocInfo = geolocator.geocode(row[3])
                            currCords = (currLocInfo.latitude, currLocInfo.longitude)
                            currDistance = geopy.distance.geodesic(self.latlongLoc, currCords).miles

                            # organizing csv dataset:
                            # row[0] == Name; row[1] == Price; row[2] == Rating; row[3] == City, State; row[4] == Latitude; row[5] == Longitude
                            # populate: locName, cityName, dist, pricePerNight, travel

                            # no distance preference
                            if self.distancepreference != 0:
                                if self.travelpreference == 'Car':
                                    #print("Found option 3") #debug
                                    opt = VacationOption()
                                    opt.populate(row[0], row[3], currDistance, row[1], driving_distance(currDistance))
                                    count += 1
                                    self.iter = count
                                    self.findOption = True
                                    reachedOption = True
                                    break

                                else:
                                    pass
                            # distance preference
                            else:
                                if self.distancepreference <= currDistance:
                                    if self.travelpreference == 'Car':
                                        #print("Found option 4") #debug
                                        opt = VacationOption()
                                        opt.populate(row[0], row[3], currDistance, row[1], driving_distance(currDistance))
                                        count += 1
                                        self.iter = count
                                        self.findOption = True
                                        reachedOption = True
                                        
                                        break
                                    else:
                                        pass
                count += 1


            if self.iter == 0 and self.findOption == False:
                self.iter = 0
                return "empty"
            
            if reachedOption == False:
                self.iter = 0
                return "empty"
                
            return opt.getAll()




input_singleton = Input()

