from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from website.input_class import input_singleton


auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        #data = request.form
        #print(data)
        budget = request.form.get("budget")
        departure = request.form.get("departure")
        return_date = request.form.get("return_date")
        starting_location = request.form.get("starting_location")
        transport_method = request.form.get("transportation")
        search_radius = request.form.get("search_radius")
        one_star = request.form.get("one_star")
        two_stars = request.form.get("two_stars")
        three_stars = request.form.get("three_stars")
        four_stars = request.form.get("four_stars")
        five_stars = request.form.get("five_stars")


        hotel_rating = []
        
        
        if one_star == 'on':
            hotel_rating.append('1')

        if two_stars == 'on':
            hotel_rating.append('2')

        if three_stars == 'on':
            hotel_rating.append('3')

        if four_stars == 'on':
            hotel_rating.append('4')

        if five_stars == 'on':
            hotel_rating.append('5') 
        

        #print("search_radius:", search_radius)
        print("transport_method:", transport_method)

        #print(budget, departure, return_date, starting_location, transport_method, search_radius, hotel_rating)

        if budget == '':
            flash('Budget is a required field.', category='error')

        present = datetime.now()

        errorcount = 0

        if departure == '':
            flash('Departure Date is a required field.', category='error')
            errorcount += 1
        else:
            departure_date_bool = datetime.strptime(departure, "%Y-%m-%d")
        
            if departure_date_bool.date() < present.date():
                flash('Input departure date occurs before today.', category='error')
                errorcount += 1

        if return_date == '':
            flash('Return Date is a required field.', category='error')
            errorcount += 1
        else:
            return_date_bool = datetime.strptime(return_date, "%Y-%m-%d")
        
            if return_date_bool.date() < present.date():
                flash('Input return date occurs before today.', category='error')
                errorcount += 1

        if starting_location == '':
            flash('Location is a required field.', category='error')
            errorcount += 1
        else:
            if ',' not in starting_location:
                flash('Make sure the location is a U.S. city in format "City, State".', category='error')
                errorcount += 1

        if transport_method == None:
            flash('Transportation Method is a required field.', category='error')
            errorcount += 1

        print("errorcount:", errorcount)
        if errorcount == 0:
            flash('Successful entries!', category='success')
            input_singleton.newInput(budget, departure, return_date, starting_location, hotel_rating, search_radius, transport_method)      
            return redirect(url_for('auth.option'))

        



    return render_template("home.html")


@auth.route('/option', methods=['GET', 'POST'])
def option():
    dis = input_singleton.getVacationOption()
    if dis == "empty":
        print("Empty")
        return render_template("no_matches_atall.html")
    
    else:
        print(dis)
        return render_template("test.html", value=dis[0], city_name=dis[1], ppn=dis[3], miles=dis[2], time=dis[4])

@auth.route('/nextoption/', methods=['GET', 'POST'])
def next_option():
    dis = input_singleton.getVacationOption()
    if dis == "empty":
        print("Empty")
        return render_template("no_matches_atall.html")
    
    else:
        print(dis)
        return render_template("test.html", value=dis[0], city_name=dis[1], ppn=dis[3], miles=dis[2], time=dis[4])
    

@auth.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")