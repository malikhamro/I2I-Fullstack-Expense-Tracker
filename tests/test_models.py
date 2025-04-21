import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dashboard.models import MigrationProgress, MigrationStatus, Base

class TestMigrationModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up in-memory SQLite database for testing
        cls.engine = create_engine('sqlite:///:memory:')
        # Create all tables
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.engine.dispose()

    def test_migration_progress_model(self):
        # Create a new MigrationProgress instance
        migration_progress = MigrationProgress(id=1, task_name="Task 1", progress=50, details="Running")
        self.session.add(migration_progress)
        self.session.commit()
        
        # Query the instance
        result = self.session.query(MigrationProgress).first()
        self.assertEqual(result.task_name, "Task 1")
        self.assertEqual(result.progress, 50)
        self.assertEqual(result.details, "Running")

    def test_migration_status_model(self):
        # Create a new MigrationStatus instance
        migration_status = MigrationStatus(id=1, status="In Progress", last_update="2023-10-01T10:00:00")
        self.session.add(migration_status)
        self.session.commit()
        
        # Query the instance
        result = self.session.query(MigrationStatus).first()
        self.assertEqual(result.status, "In Progress")
        self.assertEqual(result.last_update, "2023-10-01T10:00:00")

    def test_migration_progress_validation(self):
        # Test validation for invalid progress value
        with self.assertRaises(ValueError):
            migration_progress = MigrationProgress(id=2, task_name="Task 2", progress=-10, details="Error")

        # Test validation for missing task_name
        with self.assertRaises(ValueError):
            migration_progress = MigrationProgress(id=3, progress=20, details="Missing task name")

    def test_migration_status_validation(self):
        # Test validation for invalid status value
        with self.assertRaises(ValueError):
            migration_status = MigrationStatus(id=2, status="", last_update="2023-10-01T10:00:00")

        # Test validation for missing last_update
        with self.assertRaises(ValueError):
            migration_status = MigrationStatus(id=3, status="Complete")

if __name__ == '__main__':
    unittest.main()
