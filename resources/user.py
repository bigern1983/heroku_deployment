import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="must supply username")
    parser.add_argument("password", type=str, required=True, help="must supply password")

    
    def post(self):

        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data.get("username")):
            return {"message" : "user already exists"}, 400 #bad request 
        
        user = UserModel(**data)
        user.safe_to_db()

        return {"message": "user created succesfully"}, 201 #created 