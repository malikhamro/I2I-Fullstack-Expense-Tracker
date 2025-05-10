import pytest
from unittest.mock import patch, MagicMock
from services.permissions_service import (
    add_permission,
    remove_permission,
    assign_permission,
    revoke_permission,
    list_permissions,
    get_permission_by_role,
    update_permission
)
from models.permissions_model import Permission
from models.roles_permissions_model import RolePermission

@pytest.fixture
def new_permission():
    return {'name': 'Test Permission', 'description': 'Description of test permission'}

@pytest.fixture
def existing_permission_id():
    return 1

@pytest.fixture
def existing_role_id():
    return 1

def test_add_permission(new_permission):
    with patch('services.permissions_service.Permission') as MockPermission:
        instance = MockPermission.return_value
        instance.id = 1 
        add_permission(new_permission['name'], new_permission['description'])
        
        MockPermission.create.assert_called_once_with(name=new_permission['name'], description=new_permission['description'])

def test_remove_permission(existing_permission_id):
    with patch('services.permissions_service.Permission') as MockPermission:
        instance = MockPermission.get.return_value
        instance.delete_instance.return_value = None

        result = remove_permission(existing_permission_id)
        
        MockPermission.get.assert_called_once_with(MockPermission.id == existing_permission_id)
        instance.delete_instance.assert_called_once()
        assert result is None

def test_assign_permission(existing_role_id, existing_permission_id):
    with patch('services.permissions_service.RolePermission') as MockRolePermission:
        instance = MockRolePermission.create.return_value

        assign_permission(existing_role_id, existing_permission_id)
        
        MockRolePermission.create.assert_called_once_with(role_id=existing_role_id, permission_id=existing_permission_id)

def test_revoke_permission(existing_role_id, existing_permission_id):
    with patch('services.permissions_service.RolePermission') as MockRolePermission:
        instance = MockRolePermission.get.return_value
        instance.delete_instance.return_value = None

        revoke_permission(existing_role_id, existing_permission_id)
        
        MockRolePermission.get.assert_called_once_with(MockRolePermission.role_id == existing_role_id, MockRolePermission.permission_id == existing_permission_id)
        instance.delete_instance.assert_called_once()

def test_list_permissions():
    with patch('services.permissions_service.Permission') as MockPermission:
        MockPermission.select.return_value.dicts.return_value = [
            {'id': 1, 'name': 'Permission 1', 'description': 'Desc 1'},
            {'id': 2, 'name': 'Permission 2', 'description': 'Desc 2'},
        ]
        
        result = list_permissions()
        
        MockPermission.select.assert_called_once()
        assert len(result) == 2
        assert result[0]['name'] == 'Permission 1'
        assert result[1]['name'] == 'Permission 2'

def test_get_permission_by_role(existing_role_id):
    with patch('services.permissions_service.RolePermission') as MockRolePermission:
        with patch('services.permissions_service.Permission') as MockPermission:
            MockRolePermission.select.return_value.where.return_value.join.return_value.dicts.return_value = [
                {'id': 1, 'name': 'Permission 1', 'description': 'Desc 1'},
                {'id': 2, 'name': 'Permission 2', 'description': 'Desc 2'},
            ]
            
            result = get_permission_by_role(existing_role_id)
            
            MockRolePermission.select.assert_called_once()
            MockRolePermission.select.return_value.where.assert_called_once_with(MockRolePermission.role_id == existing_role_id)
            assert len(result) == 2
            assert result[0]['name'] == 'Permission 1'
            assert result[1]['name'] == 'Permission 2'

def test_update_permission(existing_permission_id):
    with patch('services.permissions_service.Permission') as MockPermission:
        instance = MockPermission.get.return_value
        
        new_name = 'Updated Permission'
        new_description = 'Updated description'
        result = update_permission(existing_permission_id, new_name, new_description)
        
        MockPermission.get.assert_called_once_with(MockPermission.id == existing_permission_id)
        instance.save.assert_called_once()
        assert instance.name == new_name
        assert instance.description == new_description
