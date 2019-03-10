import json

# test data
TEST_ITEM = {'itemname': 'ball', 'category': 'soccer',
             'description':'something to kick'}

def test_create_item(client):
    response = client.post('/api/v1/items', data=TEST_ITEM)
    assert response.status_code == 201
    assert response.headers['Location'] is not None

    # Invalid requests
    # blank fields should not be in input data
    response = client.post('/api/v1/items', data={'itemname': '', 'category': '',
                           'description':''})
    assert response.status_code == 400
    response = client.post('/api/v1/items', data={'itemname':' ',
                           'category':'   ', 'description':'   '})
    assert response.status_code == 400

    # Test all three fields should be present
    response = client.post('/api/v1/items', data={'itemname':'ball', 'category':'soccer'})
    assert response.status_code == 400
    response = client.post('/api/v1/items', data={'itemname':'jersey'})
    assert response.status_code == 400


def test_get_an_item(client):
    # Initial request. No data yet but request successful
    response = client.get('/api/v1/items/1')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert len(data['data']) == 0

    # Add some test data to the database
    response = client.post('/api/v1/items', data=TEST_ITEM)
    assert response.status_code == 201

    response = client.get('/api/v1/items/1')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert len(data['data']) == 1
    item = data['data'][0]
    assert len(item) > 0

    # test invalid requests
    # Non-existent id
    response = client.get('/api/v1/items/99999')
    assert response.status_code == 404
    # Invalid ID type - bad request
    response = client.get('/api/v1/items/item1')
    assert response.status_code == 400

def test_get_item_collection(client):
    response = client.get('/api/v1/items')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert not data['data'] # Nothing yet

    # Create some test_items
    response = client.post('/api/v1/items', data=TEST_ITEM)
    assert response.status_code == 201
    response = client.post('/api/v1/items', data=TEST_ITEM)
    assert response.status_code == 201

    response = client.get('/api/v1/items')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert len(data['data']) == 2

def test_patch_an_item(client):
    # Item does not exist
    response = client.patch('/api/v1/items/1/itemname',
                            data={'itemname':'new-name'})
    assert response.status_code == 404

    # create test data
    response = client.post('/api/v1/items', data=TEST_ITEM)
    assert response.status_code == 201

    # patch an item
    response = client.patch('/api/v1/items/1/itemname',
                            data={'itemname':'bat'})
    assert response.status_code == 200

    # Non-matching fields
    response = client.patch('/api/v1/items/1/itemname',
                            data={'category':'cricket'})
    assert response.status_code == 400

    # Too many fields
    response = client.patch('/api/v1/items/1/itemname',
                            data={'category':'cricket',
                                  'description': 'bowling game'})
    assert response.status_code == 400

    response = client.patch('/api/v1/items/1/itemname',
                            data={'category':'cricket',
                                  'itemname': 'bat',
                                  'description': 'blowling game'})
    assert response.status_code == 400

    # Non-existent id
    response = client.patch('/api/v1/items/1111/itemname',
                            data={'itemname':'new-name'})
    assert response.status_code == 404

    # invalid update field
    response = client.patch('/api/v1/items/1/product',
                            data={'itemname':'new-name'})
    assert response.status_code == 400

def test_delete_item(client):
    # Item does not exist
    response = client.delete('/api/v1/items/1')
    assert response.status_code == 404

    # create test data
    response = client.post('/api/v1/items', data=TEST_ITEM)
    assert response.status_code == 201

    # successful delete
    response = client.delete('/api/v1/items/1')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert data[0]['id'] == 1

    # Non-existent id
    response = client.delete('/api/v1/items/99999')
    assert response.status_code == 404

    # Invalid id type, should be an int
    response = client.delete('/api/v1/items/item-1')
    assert response.status_code == 400
