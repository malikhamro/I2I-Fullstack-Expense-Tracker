# backup_service/backup_manager.py

from backup_service.config import get_backup_settings
from backup_service.logger import log_backup_activity
import schedule
import time
import shutil
import os
from datetime import datetime

def perform_backup():
    """
    This function will handle the process of creating backups for the microservice.
    It will gather data from the database, and save it to a backup storage location.
    """
    try:
        # Retrieve backup settings
        settings = get_backup_settings()
        
        # Assuming we have a function to fetch data from the database
        data = fetch_data_from_database(settings['database_connection_string'])
        
        # Path to save the backup
        backup_path = settings['backup_storage_location']
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_file = os.path.join(backup_path, f"backup_{timestamp}.sql")
        
        # Save the fetched data to the backup location
        with open(backup_file, 'w') as file:
            file.write(data)
        
        # Log the backup activity
        log_backup_activity(f"Backup created successfully at {backup_file}. Data size: {len(data)} bytes.")
        return True

    except Exception as e:
        log_backup_activity(f"Backup failed. Error: {e}")
        return False


def schedule_backups():
    """
    This function will set up scheduled tasks to perform backups at regular intervals.
    """
    try:
        # Retrieve backup settings
        settings = get_backup_settings()
        
        # Schedule backups at the specified frequency
        backup_frequency = settings.get('backup_frequency', 'daily')

        if backup_frequency == 'daily':
            schedule.every().day.at("00:00").do(perform_backup)
        elif backup_frequency == 'weekly':
            schedule.every().monday.at("00:00").do(perform_backup)
        elif backup_frequency == 'monthly':
            schedule.every(30).days.at("00:00").do(perform_backup)
        else:
            raise ValueError("Invalid backup frequency specified in configurations.")

        # Run the scheduled jobs
        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        log_backup_activity(f"Failed to schedule backups. Error: {e}")


def fetch_data_from_database(connection_string):
    """
    Mock function to fetch data from the database.
    """
    # Connecting to the database and fetching data process (to be implemented)
    return "mock_database_data"
