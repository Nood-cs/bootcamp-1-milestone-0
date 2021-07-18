from operator import index
from flask import Flask, request, jsonify, json
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)

#This is telling our app where the DB is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'

#Initialize the DB
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, index= True)
    name = db.Column(db.String)
    cost = db.Column(db.Numeric(10,2))
    available_quantity = db.Column(db.Integer)

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item


class AddItem(Resource):   ## WORKS WELL
    def post(self):
        # request.get_json()  converts the JSON object into Python data
        # Let’s assign the incoming request data to variables and return them
        item_data = request.get_json()
        item_name = item_data['name']
        item_cost = item_data['cost']
        item_quantity = item_data['available_quantity']

        new_item = Item(name=item_name,cost=item_cost,available_quantity=item_quantity)
        
        #item_data['item_id'] = new_item.item_id
        
        try:
            db.session.add(new_item)
            db.session.commit()
            return {'message' : 'Item added successfully', 'data': item_data} ,201
        except:
            return {'message' :'There was an issue adding your task!'}
        
        
class ReadUpdateItem(Resource):
    def post(self, id):
        item_to_update = Item.query.filter_by(item_id=id).first()
        updated_item = request.get_json()

        if item_to_update is not None:
            if 'name' in updated_item:
                item_to_update.name = updated_item['name']

            if 'cost' in updated_item:
                item_to_update.cost = updated_item['cost']

            if 'available_quantity' in updated_item:
                item_to_update.available_quantity = updated_item['available_quantity']

        try:
            db.session.add(item_to_update)
            db.session.commit()
            return jsonify({'message' : 'Item updated successfully', 'data' : updated_item})
        except:
            return jsonify({'message' : 'There was an issue updating that item!'})

    def get(self, id):
        item = Item.query.filter_by(item_id=id).first()
       
        if item is None:
            return jsonify({"message" : "This item-id does not exist", "item-id": id })
        
        else:
            item_schema = ItemSchema()
            output = item_schema.dumps(item)
            
            try:
                return jsonify({'item': output})
            except:
                return jsonify({'message': 'There was an error fetching your item'})


class DeleteItem(Resource):
    def post(self, id):
        item_to_delete = Item.query.get_or_404(id)

        try:
            db.session.delete(item_to_delete)
            db.session.commit()
            return jsonify({'message' : 'Item deleted successfully'})
        except:
           return jsonify({'message' : 'There was a problem deleting that task'})


api.add_resource(AddItem, '/')
api.add_resource(ReadUpdateItem, '/readupdateitem/<int:id>')
api.add_resource(DeleteItem, '/deleteItem/<int:id>')



if __name__== '__main__':
    app.run(debug=True)
