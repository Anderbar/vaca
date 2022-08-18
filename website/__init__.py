from flask import Flask


""" creation of app for User's use """

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aasdad21234167' # dont memorize this ;) (not really important if you do)

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/') # reroute to home page

    return app

