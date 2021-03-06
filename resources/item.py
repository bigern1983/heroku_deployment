from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True, 
        help='must not be empty')
    parser.add_argument('store_id', 
        type=int, 
        required=True, 
        help='Every item needs a store_id')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item: 
            return item.json(), 200
        return {"message" :"item not found"}, 404

    
    def post(self, name):

        #check if item is already in db
        item = ItemModel.find_by_name(name)
        if item: 
            return {'message' : 'An item with name {0} already exists'.format(name)}, 400
        #if not then create it in db
        #parse request
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)


        try:
            item.save_to_db()
        except:
            return{"message" : "An error occured inserting item into database"}, 500 #internal sever error
        return item.json(), 201 #create
    

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if not item:
                item = ItemModel(name, **data)
        else: 
            item.price = data['price']
            item.store_id = data['store_id']

        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message' : 'item deleted'}, 410

class ItemList(Resource):
    def get(self):
        return {'items' : [item.json() for item in ItemModel.find_all()]}
