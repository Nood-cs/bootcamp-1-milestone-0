from flask import Flask
from flask_restful import Api
from resources.routes import initialize_routes
from models import initialize_db

app = Flask(__name__)
api = Api(app)

#This is telling our app where the DB is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merchant.db'

initialize_db(app)
initialize_routes(api)

if __name__== '__main__':
    app.run(debug=True)
