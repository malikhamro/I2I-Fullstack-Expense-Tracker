import unittest
from unittest.mock import patch
import logging
from logging/modification_logger import log_modification
from patient_data_handler import update_patient_data

class TestPatientDataHandler(unittest.TestCase):

    @patch('logging.modification_logger.log_modification')
    def test_update_patient_data_logging(self, mock_log_modification):
        user_id = 'user123'
        patient_id = 'patient456'
        old_data = {'name': 'John Doe', 'age': 30}
        new_data = {'name': 'John Smith', 'age': 31}

        # Assuming the update_patient_data function calls log_modification to log changes
        update_patient_data(user_id, patient_id, old_data, new_data)

        # Check that log_modification was called
        mock_log_modification.assert_called_once_with(
            user_id=user_id,
            patient_id=patient_id,
            modified_fields=['name', 'age'],
            old_values=old_data,
            new_values=new_data
        )

        # Verify proper logging
        log_entry = mock_log_modification.call_args[0]
        self.assertEqual(log_entry[0], user_id)
        self.assertEqual(log_entry[1], patient_id)
        self.assertListEqual(log_entry[2], ['name', 'age'])
        self.assertDictEqual(log_entry[3], old_data)
        self.assertDictEqual(log_entry[4], new_data)

if __name__ == '__main__':
    unittest.main()
