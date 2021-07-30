from flask import Flask
from flask_restful import Api
from resources.routes import initialize_routes
from models import db

def create_app(db_location):
    """
    Function that creates our Flask application.
    This function creates the Flask app, Flask-Restful API,
    and Flask-SQLAlchemy connection
    :param db_location: Connection string to the database
    :return: Initialized Flask app
    """

    app = Flask(__name__)
    api = Api(app)
    
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merchant.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_location

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    initialize_routes(api)

    return app

if __name__== '__main__':
    app = create_app('sqlite:///merchant.db')
    app.run(debug=False)
