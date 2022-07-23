from flask import Blueprint, render_template
from website.input_class import input_singleton

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/option', methods=['GET', 'POST'])
def option():
    #dis = input_singleton.getStuffTest()
    #print(dis)
    test = 'Hi'
    return render_template("test.html", value=test)
    #, city_name=dis[1], ppn=dis[3], miles=dis[2], time=dis[4])

@views.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")