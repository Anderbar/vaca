import csv
import geopy.distance
from geopy.geocoders import Nominatim
from website.vacationoption import VacationOption, VacationOptionWithFlight
#from vacationoption import VacationOption, VacationOptionWithFlight #for debug

geolocator = Nominatim(user_agent="Vaca")

# estimated travel time for driving distance
def driving_distance(dist):
    return dist/70.4


class Input:
    def __init__(self):
        self.budget = 0
        self.startDate = 0
        self.endDate = 0
        self.startLoc = 0
        self.rating = []
        self.distance_preference = 0
        self.travelpreference = 0
        #int to determine how many times we have found an option
        
        self.startLocInfo = 0
        self.latlongLoc = 0
        #bool to determine if we have found an option
        self.findOption = False
        
        self.iter = 0
        # successful options to loop through
        self.success = []
        self.curr = 0
        # determine what to return next
        self.choice = 0
        self.dateDifference = 0
        


    def newInput(self, budget, startDate, endDate, startLoc, rating, distancepreference, travelpreference, days):
        self.budget = int(budget)
        self.startDate = startDate
        self.endDate = endDate
        self.startLoc = startLoc
        self.rating = rating
        self.distancepreference = int(distancepreference)
        self.travelpreference = travelpreference
        self.startLocInfo = geolocator.geocode(self.startLoc)
        self.latlongLoc = (self.startLocInfo.latitude, self.startLocInfo.longitude)
        self.success = []
        self.curr = 0
        self.dateDifference = 0

    def testInput(self):
        self.budget = int(5000)
        self.startDate = "2022-08-22"
        self.endDate = "2022-08-24"
        self.startLoc = "Troy, NY"
        self.rating = []
        self.distancepreference = 0
        self.travelpreference = 'Plane'
        self.startLocInfo = geolocator.geocode(self.startLoc)
        self.latlongLoc = (self.startLocInfo.latitude, self.startLocInfo.longitude)
        self.success = []
        self.curr = 0
        self.dateDifference = int(2)

    # GETTERS

    def getSuccess(self):
        return self.success

    def getCurr(self):
        return self.curr

    def goBack(self):
        self.choice = 'Back'

    def goNext(self):
        self.choice = 'Next'

    def getTravelPreference(self):
        return self.travelpreference

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

    def getChoice(self):
        return self.choice

    def setChoice(self, ch):
        self.choice = ch

    def getStuffTest(self):
        return ["Marriot", "NYC", "200", "99", "2.5"]


    """
    
        The following classes pertain to the structure built in finding a Vacation Option for the User,
        They are built using some class variables that store the current option being displayed by the frontend.
        When a new option is reached, 
        - we want to update these class variables with the current location of that entry in our database
        and
        - we want to update the list of iterations within the database of options that match our User's criteria, and 
    
    """

    # get the Previous Vacation Option from the current selection of found Options

    def getPreviousOption(self):

        # error checking prior to getting previous Option

        if len(self.success) == 0:
            return -1

        if len(self.success) == 1:
            return -1

        if self.curr == self.success[0]:
            return -1

        #self.curr -= 1
        wantedOption = self.success[self.curr - 1]
        print("WantedOption:", wantedOption)

        # open database
        with open('testdata.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)

            resumeCount = 0
            for row in reader:

                if resumeCount < wantedOption - 1:
                    resumeCount += 1
                    continue

                currLocInfo = geolocator.geocode(row[3])
                currCords = (currLocInfo.latitude, currLocInfo.longitude)
                currDistance = geopy.distance.geodesic(self.latlongLoc, currCords).miles

                if self.travelpreference == 'Car':
                    opt = VacationOption()
                    opt.populate(row[0], row[3], round(currDistance), row[1], round(driving_distance(currDistance), 2), row[4])
                    break
                else:
                    opt = VacationOptionWithFlight()
                    opt.populateFlightInfo(row[0], row[3], self.startLoc, round(currDistance), row[1], self.startDate, self.endDate, row[4])
                    opt.collectAirFlightData()
                    break

        
        if self.travelpreference == 'Car':
            return opt.getAll()
        else:
            return opt.getAllWithFlight()




    # get the Next Vacation Option from the current selection of found Options

    def getNextOption(self):


        # error checking for options prior to returning a variable


        # if no options have been found, let's ignore this request
        if len(self.success) == 0:
            return -1

        # if there is only one option that has been found, let's ignore this request
        if len(self.success) == 1:
            return 2

        # if we are at the most recent option that has been found, let's ignore this request
        if self.curr == len(self.success) - 1:
            return 0


        #self.curr += 1
        wantedOption = self.success[self.curr]
        print("WantedOption:", wantedOption)

        # open database
        with open('testdata.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)

            resumeCount = 0
            for row in reader:

                if resumeCount < wantedOption - 1:
                    resumeCount += 1
                    continue

                currLocInfo = geolocator.geocode(row[3])
                currCords = (currLocInfo.latitude, currLocInfo.longitude)
                currDistance = geopy.distance.geodesic(self.latlongLoc, currCords).miles

                if self.travelpreference == 'Car':
                    opt = VacationOption()
                    opt.populate(row[0], row[3], round(currDistance), row[1], round(driving_distance(currDistance), 2), row[4])
                    break
                else:
                    opt = VacationOptionWithFlight()
                    opt.populateFlightInfo(row[0], row[3], self.startLoc, round(currDistance), row[1], self.startDate, self.endDate, row[4])
                    opt.collectAirFlightData()
                    break

        if self.travelpreference == 'Car':
            return opt.getAll()
        else:
            return opt.getAllWithFlight()



    # get a New Vacation Option to be sent to the frontend and to be sent to successful Options array

    def getVacationOption(self):
        #print("self.iter:", self.iter) # debug


        # initial variables to begin search
        count = self.iter
        resumeCount = 0
        reachedOption = False

        # open database
        with open('testdata.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            #print("length of reader:", len(reader))

            for row in reader:
                # pass through to newest entry of a found option
                if resumeCount < self.iter:
                    resumeCount += 1
                    continue

                # at this point, we are allowed to search for next options

                # budget check
                if (int(row[1]) * int(self.dateDifference)) <= self.budget:
                    #print("PRICE CHECK")
                    # rating check ( no rating requested by User )
                    if len(self.rating) == 0:
                        # distance check
                        currLocInfo = geolocator.geocode(row[3])
                        currCords = (currLocInfo.latitude, currLocInfo.longitude)
                        currDistance = geopy.distance.geodesic(self.latlongLoc, currCords).miles
                        # distance currently logged

                        # no distance preference
                        if self.distancepreference != 0:
                            if self.travelpreference == 'Car':
                                # FOUND OPTION
                                print("Found option 1") #debug
                                # updating variables before deployment of option

                                # return for frontend
                                opt = VacationOption()
                                opt.populate(row[0], row[3], round(currDistance), row[1], round(driving_distance(currDistance), 2), row[4])
                                # update vars during loop
                                count += 1
                                self.iter = count
                                self.success.append(self.iter)
                                self.curr = len(self.success) - 1
                                self.findOption = True
                                reachedOption = True
                                break

                            else:
                                if currDistance == 0:
                                    count += 1
                                    continue

                                opt = VacationOptionWithFlight()
                                opt.populateFlightInfo(row[0], row[3], self.startLoc, round(currDistance), row[1], self.startDate, self.endDate, row[4])
                                if opt.airportSameCheck() == True:
                                    count += 1
                                    continue
                                opt.collectAirFlightData()
                                if (int(row[1]) * int(self.dateDifference)) + opt.getFlightCost() > self.budget:
                                        count += 1
                                        continue
                                count += 1
                                self.iter = count
                                self.success.append(self.iter)
                                self.curr = len(self.success) - 1
                                self.findOption = True
                                reachedOption = True
                                break
                        # distance preference
                        else:
                            if self.distancepreference <= currDistance:
                                if self.travelpreference == 'Car':
                                    # FOUND OPTION
                                    # updating variables before deployment of option
                                    print("Found option 2") #debug
                                    opt = VacationOption()
                                    opt.populate(row[0], row[3], round(currDistance), row[1], round(driving_distance(currDistance), 2), row[4])
                                    count += 1
                                    self.iter = count
                                    self.success.append(self.iter)
                                    self.curr = len(self.success) - 1
                                    self.findOption = True
                                    reachedOption = True
                                    break
                                else:
                                    if currDistance == 0:
                                        count += 1
                                        continue
                                    opt = VacationOptionWithFlight()
                                    opt.populateFlightInfo(row[0], row[3], self.startLoc, round(currDistance), row[1], self.startDate, self.endDate, row[4])
                                    if opt.airportSameCheck() == True:
                                        count += 1
                                        continue
                                    opt.collectAirFlightData()
                                    if (int(row[1]) * int(self.dateDifference)) + opt.getFlightCost() > self.budget:
                                            count += 1
                                            continue
                                    count += 1
                                    self.iter = count
                                    self.success.append(self.iter)
                                    self.curr = len(self.success) - 1
                                    self.findOption = True
                                    reachedOption = True
                                    break
                    # rating check ( ratings are requested by User )
                    else:

                        if row[2] in self.rating:
                            # distance check
                            currLocInfo = geolocator.geocode(row[3])
                            currCords = (currLocInfo.latitude, currLocInfo.longitude)
                            currDistance = geopy.distance.geodesic(self.latlongLoc, currCords).miles

                            # organizing csv dataset:
                            # row[0] == Hotel; row[1] == Price; row[2] == Rating; row[3] == City, State; row[4] == Link;
                            # populate: locName, cityName, dist, pricePerNight, travel

                            # no distance preference
                            if self.distancepreference != 0:
                                if self.travelpreference == 'Car':
                                    # FOUND OPTION
                                    # updating variables before deployment of option
                                    print("Found option 3") #debug
                                    opt = VacationOption()
                                    opt.populate(row[0], row[3], round(currDistance), row[1], round(driving_distance(currDistance), 2), row[4])
                                    count += 1
                                    self.iter = count
                                    self.success.append(self.iter)
                                    self.curr = len(self.success) - 1
                                    self.findOption = True
                                    reachedOption = True
                                    break

                                else:
                                    if currDistance == 0:
                                        count += 1
                                        continue
                                    opt = VacationOptionWithFlight()
                                    opt.populateFlightInfo(row[0], row[3], self.startLoc, round(currDistance), row[1], self.startDate, self.endDate, row[4])
                                    if opt.airportSameCheck() == True:
                                        count += 1
                                        continue
                                    opt.collectAirFlightData()
                                    if (int(row[1]) * int(self.dateDifference)) + opt.getFlightCost() > self.budget:
                                            count += 1
                                            continue
                                    count += 1
                                    self.iter = count
                                    self.success.append(self.iter)
                                    self.curr = len(self.success) - 1
                                    self.findOption = True
                                    reachedOption = True
                                    break
                            # distance preference
                            else:
                                if self.distancepreference <= currDistance:
                                    if self.travelpreference == 'Car':
                                        # FOUND OPTION
                                        # updating variables before deployment of option
                                        print("Found option 4") #debug
                                        opt = VacationOption()
                                        opt.populate(row[0], row[3], round(currDistance), row[1], round(driving_distance(currDistance), 2), row[4])
                                        count += 1
                                        self.iter = count
                                        self.success.append(self.iter)
                                        self.curr = len(self.success) - 1
                                        self.findOption = True
                                        reachedOption = True
                                        
                                        break
                                    else:
                                        if currDistance == 0:
                                            count += 1
                                            continue
                                        opt = VacationOptionWithFlight()
                                        opt.populateFlightInfo(row[0], row[3], self.startLoc, round(currDistance), row[1], self.startDate, self.endDate, row[4])
                                        if opt.airportSameCheck() == True:
                                            count += 1
                                            continue
                                        opt.collectAirFlightData()
                                        if (int(row[1]) * int(self.dateDifference)) + opt.getFlightCost() > self.budget:
                                            count += 1
                                            continue
                                        count += 1
                                        self.iter = count
                                        self.success.append(self.iter)
                                        self.curr = len(self.success) - 1
                                        self.findOption = True
                                        reachedOption = True
                                        break
                count += 1

            # final checks to find solutions

            # none options found at all
            if self.iter == 0 and self.findOption == False:
                self.iter = 0
                return "empty"
            
            # last option has been found
            if reachedOption == False:
                self.iter = 0
                return "empty"
                
            if self.travelpreference == 'Car':
                return opt.getAll()
            else:
                return opt.getAllWithFlight()



# declaration of singleton class
input_singleton = Input()




# TESTING DATA; DO NOT LEAVE UNCOMMENTED FOR WEB SERVER DEPLOYMENT

"""

if __name__ == '__main__':
    input_singleton = Input()
    input_singleton.testInput()


    print()
    print("VacationOption:", input_singleton.getVacationOption())
    print()
    
    print("Success Array:", input_singleton.getSuccess())
    print("Curr Count:", input_singleton.getCurr())

    #print("NextOption:", input_singleton.getNextOption())

    print()
    print("VacationOption:", input_singleton.getVacationOption())
    print()

    print("Success Array:", input_singleton.getSuccess())
    print("Curr Count:", input_singleton.getCurr())

    

    #print("PreviousOption", input_singleton.getPreviousOption())
    #print("Success Array:", input_singleton.getSuccess())
    #print("Curr Count:", input_singleton.getCurr())

    #print("NextOption", input_singleton.getNextOption())
    #print("Success Array:", input_singleton.getSuccess())
    #print("Curr Count:", input_singleton.getCurr())



    #print("NextOption", input_singleton.getNextOption())
    #print("Success Array:", input_singleton.getSuccess())
    #print("Curr Count:", input_singleton.getCurr())
    

"""
 




