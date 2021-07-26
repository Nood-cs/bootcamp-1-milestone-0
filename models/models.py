from . import db
from sqlalchemy_serializer import SerializerMixin

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