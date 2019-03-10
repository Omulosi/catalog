import json
import pytest


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

@pytest.mark.parametrize(('path', 'data', 'invalid_field', 'invalid_id'), (
    ('/api/v1/items/1/itemname',
     {'itemname': 'new-name'},
     {'category': 'new-category'},
     '/api/v1/items/9999/itemname'
    ),
    #
    ('/api/v1/items/1/category',
     {'category': 'new-category'},
     {'itemname': 'new-name'},
     '/api/v1/items/9999/category'
    ),
    #
    ('/api/v1/items/1/description',
     {'description': 'new-description'},
     {'category': 'new-category'},
     '/api/v1/items/9999/description'
    )))
def test_patch_an_item(client, path, data, invalid_field, invalid_id):
    """ Tests for patch endpoint"""
    # Item does not exist
    response = client.patch(path, data=data)
    assert response.status_code == 404
    assert b'status' in response.data
    assert b'error' in response.data

    # create test data
    response = client.post('/api/v1/items', data=TEST_ITEM)
    assert response.status_code == 201

    # patch an item: success
    response = client.patch(path, data=data)
    assert response.status_code == 200
    resp_data = json.loads(response.data.decode('utf-8'))['data'][0]
    # check that the value in input data used to update the field is
    # present in the json response of this request
    assert True in [v in resp_data.values() for v in data.values()]

    # Non-matching fields: error
    response = client.patch(path, data=invalid_field)
    assert response.status_code == 400
    assert b'status' in response.data
    assert b'error' in response.data

    # Too many fields
    response = client.patch(path, data={'category':'cricket',
                                        'description': 'bowling game'})
    assert response.status_code == 400
    assert b'status' in response.data
    assert b'error' in response.data

    response = client.patch(path,
                            data={'category':'cricket',
                                  'itemname': 'bat',
                                  'description': 'blowling game'})
    assert response.status_code == 400
    assert b'status' in response.data
    assert b'error' in response.data

    # Non-existent id
    response = client.patch(invalid_id, data=data)
    assert response.status_code == 404
    assert b'status' in response.data
    assert b'error' in response.data

    # invalid update field
    response = client.patch('/api/v1/items/1/product',
                            data=data)
    assert response.status_code == 400
    assert b'status' in response.data
    assert b'error' in response.data

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
    data = json.loads(response.data.decode('utf-8'))['data']
    assert data[0]['id'] == 1

    # Non-existent id
    response = client.delete('/api/v1/items/99999')
    assert response.status_code == 404

    # Invalid id type, should be an int
    response = client.delete('/api/v1/items/item-1')
    assert response.status_code == 400
