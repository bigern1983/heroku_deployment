from db import db

class StoreModel(db.Model):

    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    #query builder that can retrieve items for db
    items = db.relationship('ItemModel', lazy='dynamic')


    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items':[item.json() for item in self.items.all()]}

    @classmethod #classmethod returns an object of its own type
    def find_by_name(cls, name):
        #SELECT * FROM items WHERE name=name LIMIT 1
        #get the first matching row 
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
