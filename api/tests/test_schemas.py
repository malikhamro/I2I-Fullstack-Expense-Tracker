# api/tests/test_schemas.py

import unittest
from marshmallow.exceptions import ValidationError
from api.schemas import ResourceSchema

class TestResourceSchema(unittest.TestCase):
    def setUp(self):
        self.schema = ResourceSchema()
        self.valid_data = {
            'id': 1,
            'name': 'Resource name',
            'description': 'Resource description',
            'created_at': '2023-10-01T00:00:00',
            'updated_at': '2023-10-01T00:00:00'
        }
        self.invalid_data = {
            'id': 'invalid_id',
            'name': '',
            'description': 12345,
            'created_at': 'invalid_date',
            'updated_at': 'invalid_date'
        }

    def test_serialization(self):
        serialized_data = self.schema.dump(self.valid_data)
        self.assertEqual(serialized_data['name'], 'Resource name')
        self.assertEqual(serialized_data['description'], 'Resource description')
        self.assertEqual(serialized_data['id'], 1)

    def test_deserialization(self):
        deserialized_data = self.schema.load(self.valid_data)
        self.assertEqual(deserialized_data['name'], 'Resource name')
        self.assertEqual(deserialized_data['description'], 'Resource description')
        self.assertEqual(deserialized_data['id'], 1)

    def test_validation_error_on_invalid_data(self):
        with self.assertRaises(ValidationError):
            self.schema.load(self.invalid_data)

    def test_deserialization_with_missing_required_fields(self):
        missing_fields_data = {'name': 'Resource name'}
        with self.assertRaises(ValidationError):
            self.schema.load(missing_fields_data)

if __name__ == '__main__':
    unittest.main()
