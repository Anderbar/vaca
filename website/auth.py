from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from website.input_class import input_singleton
import time


"""
    We determine some differences between frontend variables and backend variables
    by naming them different. 
    
    Backend variables remain in Camel Case
    Frontend variables will be underscore separated
    Variables that work with both frontend and backend will be underscore separated

"""


"""
    Authentication file to retrieve data and send data
    from frontend to backend
    and backend to frontend

"""


auth = Blueprint('auth', __name__)

# beginning data transfer from Frontend to Backend

@auth.route('/', methods=['GET', 'POST'])
def home():
    time.sleep(.001)
    if request.method == 'POST':
        #data = request.form
        #print(data)
        budget = request.form.get("budget")
        departure = request.form.get("departure")
        returnDate = request.form.get("return_date")
        startingLocation = request.form.get("starting_location")
        transportMethod = request.form.get("transportation")
        searchRadius = request.form.get("search_radius")
        oneStar = request.form.get("one_star")
        twoStars = request.form.get("two_stars")
        threeStars = request.form.get("three_stars")
        fourStars = request.form.get("four_stars")
        fiveStars = request.form.get("five_stars")

        # array to hold all hotel ratings if user chooses
        hotelRating = []

        # NOTE: append() adds a variable to end of the array, therefore
        # in these additions, the numbers should appear in a 
        # least to greatest order
        
        
        if oneStar == 'on':
            hotelRating.append('1')

        if twoStars == 'on':
            hotelRating.append('2')

        if threeStars == 'on':
            hotelRating.append('3')

        if fourStars == 'on':
            hotelRating.append('4')

        if fiveStars == 'on':
            hotelRating.append('5') 
        

        #print("search_radius:", search_radius) #debug
        print("transportMethod:", transportMethod)

        #print(budget, departure, return_date, starting_location, transport_method, search_radius, hotel_rating) #debug


        # ERROR MESSAGING TO FRONTEND


        # empty budget
        if budget == '':
            flash('Budget is a required field.', category='error')

        present = datetime.now()

        errorcount = 0

        # empty departure date
        if departure == '':
            flash('Departure Date is a required field.', category='error')
            errorcount += 1

        else:

            # check if date is before whatever today is
            departureDateBool = datetime.strptime(departure, "%Y-%m-%d")

            if departureDateBool.date() < present.date():
                flash('Input departure date occurs before today.', category='error')
                errorcount += 1

        # empty return date
        if returnDate == '':
            flash('Return Date is a required field.', category='error')
            errorcount += 1

        else:

            # check if date is before whatever today is
            returnDateBool = datetime.strptime(returnDate, "%Y-%m-%d")
        
            if returnDateBool.date() < present.date():
                flash('Input return date occurs before today.', category='error')
                errorcount += 1

        # empty start location
        if startingLocation == '':
            flash('Location is a required field.', category='error')
            errorcount += 1
        else:
            if ',' not in startingLocation:
                flash('Make sure the location is a U.S. city in format "City, State".', category='error')
                errorcount += 1

        # if empty transportation method
        if transportMethod == None:
            flash('Transportation Method is a required field.', category='error')
            errorcount += 1

        #print("errorcount:", errorcount) #debug

        # No errors! If this point is reached, we can proceed to work with the backend
        if errorcount == 0:
            flash('Successful entries!', category='success')
            delta = departureDateBool - returnDateBool
            input_singleton.newInput(budget, departure, returnDate, startingLocation, hotelRating, searchRadius, transportMethod, delta.days)      
            return redirect(url_for('auth.option'))

    return render_template("home.html")


"""
@auth.route('/', methods=['GET', 'POST'])
def testing():
    return(render_template("test_flight.html"))
"""

# initial give option
@auth.route('/option', methods=['GET', 'POST'])
def option():
    check = input_singleton.getVacationOption()
    if check == "empty":
        print("Empty")
        return render_template("no_matches_atall.html")
    
    else:
        print(check)
        if input_singleton.getTravelPreference() == 'Car':
            return render_template("test.html", value=check[0], city_name=check[1], ppn=check[3], miles=check[2], time=check[4], hotel_link=check[5])
        else:
            return render_template("test_flight.html", value=check[0], city_name=check[1], ppn=check[3], miles=check[2], time=check[4], start_airport=check[6], end_airport=check[7], airline=check[5], flight_number=check[8], flight_cost=check[10], return_airline=check[12], return_flight_number=check[11], hotel_link=check[13], flight_link=check[9])

# new or next option (Backend to Frontend)
@auth.route('/nextoption/', methods=['GET', 'POST'])
def next_option():

    
    check = input_singleton.getNextOption()
    if check == 0 or check == 2:
        check = input_singleton.getVacationOption()
    if check == -1:
        print("Empty")
        return render_template("no_matches_atall.html")

    if check == "empty":
        print("Empty")
        return render_template("no_matches_atall.html")

    if check != "empty" or check != 0 or check != 2 or check != -1:
        print(check)
        if input_singleton.getTravelPreference() == 'Car':
            return render_template("test.html", value=check[0], city_name=check[1], ppn=check[3], miles=check[2], time=check[4], hotel_link=check[5])
        else:
            return render_template("test_flight.html", value=check[0], city_name=check[1], ppn=check[3], miles=check[2], time=check[4], start_airport=check[6], end_airport=check[7], airline=check[5], flight_number=check[8], flight_cost=check[10], return_airline=check[12], return_flight_number=check[11], hotel_link=check[13], flight_link=check[9])

# previous option (Backend to Frontend)
@auth.route('/backoption/', methods=['GET', 'POST'])
def back_option():
    check = input_singleton.getPreviousOption()
    if check == -1:
        return render_template("no_matches_atall.html")
    else:
        print(check)
        if input_singleton.getTravelPreference() == 'Car':
            return render_template("test.html", value=check[0], city_name=check[1], ppn=check[3], miles=check[2], time=check[4], hotel_link=check[5])
        else:
            return render_template("test_flight.html", value=check[0], city_name=check[1], ppn=check[3], miles=check[2], time=check[4], start_airport=check[6], end_airport=check[7], airline=check[5], flight_number=check[8], flight_cost=check[10], return_airline=check[12], return_flight_number=check[11], hotel_link=check[13], flight_link=check[9])
            #return [self.locName, self.cityName, round(self.dist), self.pricePerNight, round(self.travelTime, 2), self.airlineName, self.startAirport, self.endAirport, self.flightName, self.flightLink]
    
# go to about page if clicked :)
@auth.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")