import unittest

# Assuming the status_tracker.py is already implemented with the initialize_status_tracker function
from dashboard.status_tracker import initialize_status_tracker

class TestStatusTracker(unittest.TestCase):

    def test_initialize_status_tracker(self):
        # Act
        status = initialize_status_tracker()

        # Assert
        self.assertIsInstance(status, dict, "The status should be a dictionary.")
        self.assertIn('task1', status, "The status dictionary should include 'task1' as a key.")
        self.assertIn('task2', status, "The status dictionary should include 'task2' as a key.")
        self.assertTrue(all(isinstance(val, bool) for val in status.values()), "All values in the status dictionary should be boolean.")

if __name__ == '__main__':
    unittest.main()
