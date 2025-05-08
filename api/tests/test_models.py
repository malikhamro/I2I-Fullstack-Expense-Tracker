# api/tests/test_models.py

import pytest
from api.models import db, ResourceModel

# Helper function to create a Resource instance
def create_resource(session, **kwargs):
    resource = ResourceModel(**kwargs)
    session.add(resource)
    session.commit()
    return resource

@pytest.fixture
def init_db():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

def test_ResourceModel_creation(init_db):
    resource_data = {
        "name": "Test Resource",
        "description": "This is a test resource",
        # Assuming there are more fields, add them here
    }
    
    resource = create_resource(db.session, **resource_data)
    fetched_resource = ResourceModel.query.get(resource.id)

    assert fetched_resource is not None
    assert fetched_resource.name == resource_data["name"]
    assert fetched_resource.description == resource_data["description"]
    # Add more assertions based on the fields of ResourceModel

def test_ResourceModel_update(init_db):
    resource_data = {
        "name": "Test Resource",
        "description": "This is a test resource",
        # Assuming there are more fields, add them here
    }
    
    resource = create_resource(db.session, **resource_data)

    update_data = {
        "name": "Updated Test Resource",
        "description": "This is an updated test resource",
        # Assuming there are more fields, add them here
    }

    for key, value in update_data.items():
        setattr(resource, key, value)

    db.session.commit()
    
    updated_resource = ResourceModel.query.get(resource.id)

    assert updated_resource.name == update_data["name"]
    assert updated_resource.description == update_data["description"]
    # Add more assertions based on the fields of ResourceModel

def test_ResourceModel_delete(init_db):
    resource_data = {
        "name": "Test Resource",
        "description": "This is a test resource",
        # Assuming there are more fields, add them here
    }
    
    resource = create_resource(db.session, **resource_data)

    db.session.delete(resource)
    db.session.commit()

    deleted_resource = ResourceModel.query.get(resource.id)
    assert deleted_resource is None
