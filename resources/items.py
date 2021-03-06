from flask import request, abort
from flask_restful import Resource
from models import db
from models.models import Item

# Create Item
class AddItem(Resource):
    def post(self):
        
        body = request.get_json()
        item_name = body['name']
        item_cost = body['cost']
        item_quantity = body['available_quantity']

        new_item = Item(name=item_name,cost=item_cost,available_quantity=item_quantity)
       
        try:
            db.session.add(new_item)
            db.session.commit()
            
            return {'message' : 'Item added successfully', 'data': body} ,201
        
        except:
            return {'message' :'There was an issue adding your task!'}, 422
        
# Read Item
class ReadItem(Resource):
    def get(self, id):
        try:
            item = Item.query.get(id)
            
            #isExist_item(item)
            if item is None:
                return {'message' : 'Item not found'}, 404

            output = item.to_dict()
            
            return {'item': output}, 201
        
        except:
            return {'message': 'There was an error fetching your item'}, 422

# Update Item
class UpdateItem(Resource):
    def put(self, id):
        body = request.get_json()
       
        try:
            item_to_update = Item.query.get(id)

            # isExist_item(item_to_update)
            if item_to_update is None:
                return {'message' : 'Item not found'}, 404

            if 'name' in body:
                item_to_update.name = body['name']

            if 'cost' in body:
                item_to_update.cost = body['cost']

            if 'available_quantity' in body:
                item_to_update.available_quantity = body['available_quantity']

            db.session.commit()
            return {'Item Updated' : body}, 201
        
        except:
            return {'message' : 'There was an issue updating that item!'}, 422

# Delete Item
class DeleteItem(Resource):
    def delete(self, id):
        try:
            item_to_delete = Item.query.get(id)

            #isExist_item(item_to_delete)
            if item_to_delete is None:
                return {'message' : 'Item not found'}, 404

            db.session.delete(item_to_delete)
            db.session.commit()
            
            return {'message' : 'Item deleted successfully'} , 201
       
        except:
           return {'message' : 'There was a problem deleting that task'}, 422

def isExist_item(item: Item):
    if item is None:
        abort(404, 'item not found')