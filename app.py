from operator import index
from flask import Flask, request, jsonify, json
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
api = Api(app)

#This is telling our app where the DB is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items1.db'

#Initialize the DB
db = SQLAlchemy(app)

class Item(db.Model, SerializerMixin):
    item_id = db.Column(db.Integer, primary_key=True, index= True)
    name = db.Column(db.String)
    cost = db.Column(db.Numeric(10,2))
    available_quantity = db.Column(db.Integer)

# Create Item
class AddItem(Resource):
    def post(self):
        
        # request.get_json()  converts the JSON object into Python data
        # Let’s assign the incoming request data to variables and return them
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
        
# Method ['GET'] - Read  Item
# Method ['PUT'] - Update Item
class ReadUpdateItem(Resource):
    def put(self, id):
        body = request.get_json()
       
        try:
            item_to_update = Item.query.get(id)

            if item_to_update is None:
                return {'message' : 'Item id does not exist to be updated!'}, 404
           
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

    def get(self, id):
        try:
            item = Item.query.get(id)
            if item is None:
                return {"message" : "This item-id does not exist" }, 404
        
            output = item.to_dict()
            
            return {'item': output}, 201
        
        except:
            return {'message': 'There was an error fetching your item'}, 422

# Delete Item
class DeleteItem(Resource):
    def delete(self, id):
        try:
            item_to_delete = Item.query.get(id)

            if item_to_delete is None:
                return {"message" : "This item-id does not exist"}, 404
        
            db.session.delete(item_to_delete)
            db.session.commit()
            
            return {'message' : 'Item deleted successfully'} , 201
       
        except:
           return {'message' : 'There was a problem deleting that task'}, 422


api.add_resource(AddItem, '/item')
api.add_resource(ReadUpdateItem, '/items/<int:id>')
api.add_resource(DeleteItem, '/items/<int:id>')



if __name__== '__main__':
    app.run(debug=True)
