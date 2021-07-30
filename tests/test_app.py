
def test_add_item(client):
    new_items =[
        {
            "name": "itemX",
            "cost": 25,
            "available_quantity": 15
        },
        {
            "name": "itemY",
            "cost": 30,
            "available_quantity": 9
        },
        {
            "name": "itemZ",
            "cost": 15,
            "available_quantity": 3
        }]
        

    response = client.post('/items/', json= new_items[0],
        content_type='application/json')
    assert response.status_code == 201
    # assert response.data == jsonify({
    #     'message' : 'Item added successfully',
    #     'data' :  {
    #         "name": "itemX",
    #         "cost": 25,
    #         "available_quantity": 15
    #     }
    # })

    # response = client.post('/items/', json=new_items[1],
    #     content_type='application/json')
    # assert response.status_code == 201
    # assert rassert response.data == jsonify({
    #     'message' : 'Item added successfully',
    #     'data' :  {
    #         "name": "itemY",
    #         "cost": 30,
    #         "available_quantity": 9
    #     }
    # })

    # response = client.post('/items/', json=new_items[2],
    #     content_type='application/json')
    # assert response.status_code == 201
    # assert response.data == jsonify({
    #     'message' : 'Item added successfully',
    #     'data' :  {
    #         "name": "itemZ",
    #         "cost": 15,
    #         "available_quantity": 3
    #     }
    # })
   

def test_read_item(client):
    response = client.get('/items/1')
    assert response.status_code == 201
    # assert response.data == jsonify({
    #     "item":
    #         {
    #             "name": "Apple",
    #             "cost": 25,
    #             "available_quantity": 15
    #         }
    # })

def test_read_notfound_item(client):
    response = client.get('/items/5')
    assert response.status_code == 404
    # assert response.data == jsonify({"message" : "item is not found"})

def test_update_item(client):
    response = client.put('/items/1',
    json={
            "available_quantity": 10
        })
    assert response.status_code == 201
    #assert response.data == jsonify({
    #     "Item Updated": {
    #         "available_quantity": 10
    #     }
    # })

def test_update_notfound_item(client):
    response = client.put('/items/5',
    json={
            "available_quantity": 10
        })
    assert response.status_code == 404
    #assert response.data == jsonify({"message" : "item is not found"})

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

def test_update_order(client):
    update_order = { 
            "item_id": 1,
            "shopping_cart_id": 1,
            "requested_quantity": 3
        }
    response = client.put('/orders/1', json= update_order,
        content_type='application/json')
    assert response.status_code == 201

def test_noavailqty_order(client):
    update_order = { 
            "item_id": 1,
            "shopping_cart_id": 1,
            "requested_quantity": 100
        }
    response = client.put('/orders/1', json= update_order,
        content_type='application/json')
    assert response.status_code == 422

def test_notfounditem_order(client):
    update_order = {
            "item_id": 3,
            "shopping_cart_id": 1,
            "requested_quantity": 100
        }
    response = client.put('/orders/1', json= update_order,
        content_type='application/json')
    assert response.status_code == 422

def test_read_order(client):
    response = client.get('/orders/1')
    assert response.status_code == 201

def test_read_notfound_order(client):
    response = client.get('/orders/1')
    assert response.status_code == 201

################ clean up test database orders
def test_delete_notfound_order(client):
    response = client.delete('/orders/5')
    assert response.status_code == 404

def test_delete_order(client):
    response = client.delete('/orders/1')
    assert response.status_code == 201


################# clean up test database items
def test_delete_item(client):
    response = client.delete('/items/1')
    assert response.status_code == 201
    #assert response.data == jsonify({"message" : "Item deleted successfully"})

def test_delete_notfound_item(client):
    response = client.delete('/items/5')
    assert response.status_code == 404
    #assert response.data == jsonify({"message" : "Item is not found"})    