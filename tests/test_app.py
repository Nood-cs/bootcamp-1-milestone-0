
def test_add_item(client):
    new_items =[
        {
            "name": "itemX",
            "cost": 25.00,
            "available_quantity": 15
        },
        {
            "name": "itemY",
            "cost": 30.00,
            "available_quantity": 9
        },
        {
            "name": "itemZ",
            "cost": 15.00,
            "available_quantity": 3
        }]
        

    response = client.post('/items/', json= new_items[0],
        content_type='application/json')
    assert response.status_code == 201
    assert response.json == {
        'message' : 'Item added successfully',
        'data' :  {
            "name": "itemX",
            "cost": 25.00,
            "available_quantity": 15
        }
    }

    response = client.post('/items/', json=new_items[1],
        content_type='application/json')
    assert response.status_code == 201
    assert response.json == {
        'message' : 'Item added successfully',
        'data' :  {
            "name": "itemY",
            "cost": 30.00,
            "available_quantity": 9
        }
    }

    response = client.post('/items/', json=new_items[2],
        content_type='application/json')
    assert response.status_code == 201
    assert response.json == {
        'message' : 'Item added successfully',
        'data' :  {
            "name": "itemZ",
            "cost": 15.00,
            "available_quantity": 3
        }
    }
   

def test_read_item(client):
    response = client.get('/items/1')
    assert response.status_code == 201
    assert response.json == {
        "item":
            {
                "item_id": 1,
                "name": "itemX",
                "cost": '25.00',
                "available_quantity": 15
            }
    }

def test_read_notfound_item(client):
    response = client.get('/items/5')
    assert response.status_code == 404
    assert response.json == {"message" : "Item not found"}

def test_update_item(client):
    response = client.put('/items/1',
    json={
            "available_quantity": 10
        })
    assert response.status_code == 201
    assert response.json == {
        "Item Updated": {
            "available_quantity": 10
        }
    }

def test_update_notfound_item(client):
    response = client.put('/items/5',
    json={
            "available_quantity": 10
        })
    assert response.status_code == 404
    assert response.json == {"message" : "Item not found"}

###### Test Orders ######

def test_add_order(client):
    new_order = { 
            "item_id": 1,
            "shopping_cart_id": 1,
            "requested_quantity": 8
        }
    response = client.post('/orders/', json= new_order,
        content_type='application/json')
    assert response.status_code == 201
    assert response.json == {
        'message': 'Order added successfully',
        'data':{
            "item_id": 1,
            "shopping_cart_id": 1,
            "requested_quantity": 8
        }
    }

def test_update_order(client):
    update_order = { 
            "item_id": 1,
            "shopping_cart_id": 1,
            "requested_quantity": 3
        }
    response = client.put('/orders/1', json= update_order,
        content_type='application/json')
    assert response.status_code == 201
    assert response.json =={
        'Order Updated':{
            "item_id": 1,
            "shopping_cart_id": 1,
            "requested_quantity": 3
        }
    }

def test_noavailqty_order(client):
    update_order = { 
            "item_id": 1,
            "shopping_cart_id": 1,
            "requested_quantity": 100
        }
    response = client.put('/orders/1', json= update_order,
        content_type='application/json')
    assert response.status_code == 422
    assert response.json =={'message':'There was an issue updating that Order!'}

def test_notfounditem_order(client):
    update_order = {
            "item_id": 3,
            "shopping_cart_id": 1,
            "requested_quantity": 100
        }
    response = client.put('/orders/1', json= update_order,
        content_type='application/json')
    assert response.status_code == 422
    assert response.json =={'message':'There was an issue updating that Order!'}

def test_read_order(client):
    response = client.get('/orders/1')
    assert response.status_code == 201
    assert response.json =={
        "order":
            {
                'item':{'available_quantity': 7,
                        'cost': '25.00',
                        'item_id': 1,
                        'name': 'itemX'},
                "order_id": 1,
                "item_id": 1,
                "shopping_cart_id": 1,
                "requested_quantity": 3,
                "total_cost": '75.00'
            }
        }


def test_read_notfound_order(client):
    response = client.get('/orders/2')
    assert response.status_code == 404
    assert response.json =={'message':'order is not found'}

################ clean up test database orders
def test_delete_notfound_order(client):
    response = client.delete('/orders/5')
    assert response.status_code == 404
    assert response.json =={'message':'order is not found'}
    
def test_delete_order(client):
    response = client.delete('/orders/1')
    assert response.status_code == 201
    assert response.json =={'message':'Order deleted successfully'}
    

################# clean up test database items
def test_delete_item(client):
    response = client.delete('/items/1')
    assert response.status_code == 201
    assert response.json == {"message" : "Item deleted successfully"}

def test_delete_notfound_item(client):
    response = client.delete('/items/5')
    assert response.status_code == 404
    assert response.json == {"message" : "Item not found"}