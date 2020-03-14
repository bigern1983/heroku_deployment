from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from models.user import UserModel

from db import db

if __name__ == '__main__':

    app = Flask(__name__)
    #turn of flasks modification tracker it's wasting resources
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.secret_key = 'password'
    api = Api(app)

    @app.before_first_request
    def create_tables():
        #creates everything automatically
        db.create_all()

    #creates an endpoint /auth 
    #takes a username and password and sends to authenticate
    jwt = JWT(app, authenticate, identity)

    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(Item, '/item/<string:name>') #http://localhost:5000/student/adam
    api.add_resource(ItemList, '/items')
    api.add_resource(UserRegister, '/register')
    api.add_resource(StoreList, '/stores')
    db.init_app(app)
    
    app.run(port = 5000, debug = True)


