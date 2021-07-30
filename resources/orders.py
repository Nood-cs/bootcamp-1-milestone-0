from flask import request, abort
from flask_restful import Resource
from models import db
from models.models import Item, Order
from .items import isExist_item

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
            #isExist_order(order)
            
            if order is None:
               return {'message': 'order is not found'}, 404

            output = order.to_dict()
            
            return {'order': output}, 201
        
        except:
            return {'message': 'There was an error fetching your order'}, 422

class UpdateOrder(Resource):
    def put(self, id):
        body = request.get_json()
       
        try:
            order_to_update = Order.query.get(id)
            
            #isExist_order(order_to_update)
            
            if order_to_update is None:
               return {'message': 'order is not found'}, 404

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
            #isExist_order(order_to_delete)
            
            if order_to_delete is None:
               return {'message': 'order is not found'}, 404

            item = Item.query.get(order_to_delete.item_id)

            item.available_quantity = Update_item(item, -order_to_delete.requested_quantity)

            db.session.delete(order_to_delete)
            db.session.commit()

            return {'message' : 'Order deleted successfully'} , 201

        except:
            return {'message' : 'There was a problem deleting that order'}, 422

def isExist_order(ordr: Order):
    if ordr is None:
        abort(404, 'order is not found')

def isavailable_qty(item: Item, rqstdqty: int):
    isExist_item(item)
    if item.available_quantity < rqstdqty:
        abort(422, 'No available quantity')

def Update_item(item: Item, rqstdqty: int):
    return item.available_quantity - rqstdqty; 

def calc_total_cost(item: Item, rqstdqty: int):
    return item.cost * rqstdqty