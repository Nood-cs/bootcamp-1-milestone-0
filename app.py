from flask import Flask, request, jsonify, json, abort
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
api = Api(app)

#This is telling our app where the DB is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merchant.db'

#Initialize the DB
db = SQLAlchemy(app)

class Item(db.Model, SerializerMixin):
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    cost = db.Column(db.Numeric(10,2))
    available_quantity = db.Column(db.Integer)

class Order(db.Model, SerializerMixin):
    order_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'))
    shopping_cart_id = db.Column(db.Integer)
    requested_quantity = db.Column(db.Integer)    
    total_cost = db.Column(db.Numeric(10,2))
    item = db.relationship('Item')  #Many to one relationship

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
        
# Read Item
class ReadItem(Resource):
    def get(self, id):
        try:
            item = Item.query.get(id)
            if item is None:
                return {"message" : "This item-id does not exist" }, 404
        
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

# Create Order
class CreateOrder(Resource):
    def post(self):
        body = request.get_json()
        item_id = body['item_id']
        shopping_cart_id = body['shopping_cart_id']
        requested_quantity = body['requested_quantity']
        
        item = Item.query.get(item_id)
        
        isavailable_qty(item, requested_quantity)
        
        item.available_quantity = Update_item(item, requested_quantity)

        total_cost = calc_total_cost(item, requested_quantity)

        new_order = Order(item_id=item_id,
                        shopping_cart_id=shopping_cart_id,
                        requested_quantity=requested_quantity, total_cost= total_cost)
       
        try:
            db.session.add(new_order)
            db.session.commit()
            
            return {'message' : 'Order added successfully', 'data': body} ,201
        
        except:
            return {'message' :'There was an issue added your order!'}, 422

class ReadOrder(Resource):
    def get(self, id):
        try:
            order = Order.query.get(id)
            
            if order is None:
                return {"message" : "Order is not found" }, 404
        
            output = order.to_dict()
            
            return {'order': output}, 201
        
        except:
            return {'message': 'There was an error fetching your order'}, 422

class UpdateOrder(Resource):
    def put(self, id):
        body = request.get_json()
       
        try:
            order_to_update = Order.query.get(id)
            
            if order_to_update is None:
                return {'message' : 'Order is not found'}, 404
           
            if 'shopping_cart_id' in body:
                order_to_update.shopping_cart_id = body['shopping_cart_id']

            if 'item_id' in body:
                order_to_update.item_id = body['item_id']
            
            if 'requested_quantity' in body:
                
                #get the item
                item = Item.query.get(order_to_update.item_id) 

                #check if available
                isavailable_qty(item, body['requested_quantity'] - order_to_update.requested_quantity)
                
                #update item available quantity
                item.available_quantity = Update_item(item, body['requested_quantity'] - order_to_update.requested_quantity)
                
                #update order quantity
                order_to_update.requested_quantity = body['requested_quantity']

            #calculate order total cost
            order_to_update.total_cost = calc_total_cost(item, order_to_update.requested_quantity)
            
            db.session.commit()
            return {'Order Updated' : body}, 201
        
        except:
            return {'message' : 'There was an issue updating that Order!'}, 422


class DeleteOrder(Resource):
    def delete(self, id):
        try:
            order_to_delete = Order.query.get(id)
            if order_to_delete is None:
                return {"message" : "Order is not found"}, 404

            item = Item.query.get(order_to_delete.item_id)

            item.available_quantity = Update_item(item, -order_to_delete.requested_quantity)

            db.session.delete(order_to_delete)
            db.session.commit()

            return {'message' : 'Order deleted successfully'} , 201

        except:
            return {'message' : 'There was a problem deleting that order'}, 422


def isavailable_qty(item: Item, rqstdqty: int):
    if item is None:
        abort(404, 'item is not found')
    if item.available_quantity < rqstdqty:
        abort(422, 'No available quantity')

def Update_item(item: Item, rqstdqty: int):
    return item.available_quantity - rqstdqty; 

def calc_total_cost(item: Item, rqstdqty: int):
    return item.cost * rqstdqty

api.add_resource(AddItem, '/item')
api.add_resource(ReadItem, '/items/<int:id>')
api.add_resource(UpdateItem, '/items/<int:id>')
api.add_resource(DeleteItem, '/items/<int:id>')

api.add_resource(CreateOrder, '/order')
api.add_resource(ReadOrder, '/orders/<int:id>')
api.add_resource(UpdateOrder, '/orders/<int:id>')
api.add_resource(DeleteOrder, '/orders/<int:id>')

if __name__== '__main__':
    app.run(debug=True)
