
import sqlite3
from db import db

class UserModel(db.Model):

    #configure SQLAlchemy 
    __tablename__ = 'users'
    #id is auto completed by sqlalchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    def __init__(self, username, password):
        #must match the class variable names above
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id)

    def safe_to_db(self):
        db.session.add(self)
        db.session.commit()
