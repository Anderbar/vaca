from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aasdad21234167'

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    return app

