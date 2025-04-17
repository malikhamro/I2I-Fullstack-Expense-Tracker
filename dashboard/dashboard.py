# dashboard/dashboard.py

from dashboard.ui_elements import setup_ui_elements
from dashboard.progress_tracker import initialize_progress_tracker
from dashboard.status_tracker import initialize_status_tracker
from utils.data_fetcher import fetch_migration_data
from utils.data_analyzer import analyze_migration_data
from utils.data_updater import update_dashboard_data

def create_dashboard():
    """
    Creates the initial setup for the monitoring dashboard including UI elements and layout.
    It initializes components related to tracking progress and status of data migration.
    """
    try:
        # Setup the UI elements required for the dashboard
        setup_ui_elements()

        # Initialize the progress tracker
        initialize_progress_tracker()

        # Initialize the status tracker
        initialize_status_tracker()

        # Fetch the initial migration data
        migration_data = fetch_migration_data()
        if migration_data is None:
            raise ValueError("Failed to fetch initial migration data")

        # Analyze the fetched migration data
        analyzed_data = analyze_migration_data(migration_data)
        if analyzed_data is None:
            raise ValueError("Failed to analyze initial migration data")

        # Update the dashboard with the analyzed data
        update_dashboard_data(analyzed_data)

        print("Dashboard setup completed successfully.")
    except Exception as e:
        print(f"Error during dashboard setup: {e}")
        # Implement logging and additional error handling as needed

# Execute the function to create the dashboard when the script is run
if __name__ == "__main__":
    create_dashboard()
