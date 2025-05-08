import json
import pytest
from api.models import db, ResourceModel
from api.schemas import ResourceSchema
from api.app import create_app

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

@pytest.fixture(scope='function')
def add_sample_resource():
    def _add_sample_resource(data):
        resource = ResourceModel(**data)
        db.session.add(resource)
        db.session.commit()
        return resource
    return _add_sample_resource

def test_get_resources(test_client, add_sample_resource):
    resource_data = {'name': 'Sample Resource', 'description': 'Sample Description'}
    add_sample_resource(resource_data)

    response = test_client.get('/resources')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['name'] == resource_data['name']
    assert data[0]['description'] == resource_data['description']

def test_get_resource(test_client, add_sample_resource):
    resource_data = {'name': 'Sample Resource', 'description': 'Sample Description'}
    resource = add_sample_resource(resource_data)

    response = test_client.get(f'/resources/{resource.id}')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['name'] == resource_data['name']
    assert data['description'] == resource_data['description']

def test_create_resource(test_client):
    resource_data = {'name': 'New Resource', 'description': 'New Description'}

    response = test_client.post('/resources', data=json.dumps(resource_data), content_type='application/json')
    assert response.status_code == 201

    data = json.loads(response.data)
    assert data['name'] == resource_data['name']
    assert data['description'] == resource_data['description']

    resource_in_db = ResourceModel.query.get(data['id'])
    assert resource_in_db is not None
    assert resource_in_db.name == resource_data['name']
    assert resource_in_db.description == resource_data['description']

def test_update_resource(test_client, add_sample_resource):
    resource_data = {'name': 'Sample Resource', 'description': 'Sample Description'}
    updated_data = {'name': 'Updated Resource', 'description': 'Updated Description'}
    resource = add_sample_resource(resource_data)

    response = test_client.put(f'/resources/{resource.id}', data=json.dumps(updated_data), content_type='application/json')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['name'] == updated_data['name']
    assert data['description'] == updated_data['description']

    resource_in_db = ResourceModel.query.get(resource.id)
    assert resource_in_db.name == updated_data['name']
    assert resource_in_db.description == updated_data['description']

def test_delete_resource(test_client, add_sample_resource):
    resource_data = {'name': 'Sample Resource', 'description': 'Sample Description'}
    resource = add_sample_resource(resource_data)

    response = test_client.delete(f'/resources/{resource.id}')
    assert response.status_code == 204

    resource_in_db = ResourceModel.query.get(resource.id)
    assert resource_in_db is None
