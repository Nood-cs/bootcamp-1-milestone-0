from .items import AddItem, DeleteItem, ReadItem, UpdateItem
from .orders import CreateOrder, ReadOrder, DeleteOrder, UpdateOrder

def initialize_routes(api):
    api.add_resource(AddItem, '/items/')
    api.add_resource(ReadItem, '/items/<int:id>')
    api.add_resource(UpdateItem, '/items/<int:id>')
    api.add_resource(DeleteItem, '/items/<int:id>')

    api.add_resource(CreateOrder, '/orders/')
    api.add_resource(ReadOrder, '/orders/<int:id>')
    api.add_resource(UpdateOrder, '/orders/<int:id>')
    api.add_resource(DeleteOrder, '/orders/<int:id>')