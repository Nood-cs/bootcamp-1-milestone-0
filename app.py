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
        item_data = request.get_json()
        item_name = item_data['name']
        item_cost = item_data['cost']
        item_quantity = item_data['available_quantity']

        new_item = Item(name=item_name,cost=item_cost,available_quantity=item_quantity)
       
        try:
            db.session.add(new_item)
            db.session.commit()
            return {'message' : 'Item added successfully', 'data': item_data} ,201
        except:
            return {'message' :'There was an issue adding your task!'}
        
# Method ['GET'] - Read  Item
# Method ['PUT'] - Update Item
class ReadUpdateItem(Resource):
    def put(self, id):
        item_to_update = Item.query.get(id)
        updated_item = request.get_json()

        if item_to_update is not None:
            if 'name' in updated_item:
                item_to_update.name = updated_item['name']

            if 'cost' in updated_item:
                item_to_update.cost = updated_item['cost']

            if 'available_quantity' in updated_item:
                item_to_update.available_quantity = updated_item['available_quantity']

            try:
                db.session.commit()
                return {'Item Updated' : updated_item}, 201
            except:
                return {'message' : 'There was an issue updating that item!'}
        else:
             return {'message' : 'Item id does not exist to be updated!'}, 404

    def get(self, id):
        item = Item.query.get(id)
       
        if item is None:
            return {"message" : "This item-id does not exist" }, 404
        
        else:
            output = item.to_dict()
            
            try:
                return {'item': output}, 201
            except:
                return {'message': 'There was an error fetching your item'}

# Delete Item
class DeleteItem(Resource):
    def post(self, id):
        item_to_delete = Item.query.filter_by(item_id=id).first()

        if item_to_delete is None:
          return {"message" : "This item-id does not exist"}, 404
        
        try:
            db.session.delete(item_to_delete)
            db.session.commit()
            return {'message' : 'Item deleted successfully'} , 201
        except:
           return {'message' : 'There was a problem deleting that task'}


api.add_resource(AddItem, '/item')
api.add_resource(ReadUpdateItem, '/get_item/<int:id>', '/update_item/<int:id>')
api.add_resource(DeleteItem, '/delete_item/<int:id>')



if __name__== '__main__':
    app.run(debug=True)
