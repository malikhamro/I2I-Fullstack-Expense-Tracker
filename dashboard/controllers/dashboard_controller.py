# dashboard/controllers/dashboard_controller.py

from dashboard.services.data_service import fetch_migration_data, aggregate_migration_data
from dashboard.services.status_service import check_migration_status

def update_dashboard_view():
    """
    Updates the data shown in the dashboard based on the latest migration data.
    
    Retrieves fresh migration data, aggregates it, and updates the dashboard view.
    """
    try:
        # Fetch the latest migration data
        migration_data = fetch_migration_data()
        if not migration_data:
            raise ValueError("No migration data available.")

        # Aggregate migration data for the dashboard
        aggregated_data = aggregate_migration_data(migration_data)
        if not aggregated_data:
            raise ValueError("Failed to aggregate migration data.")

        # Here, normally we would update the dashboard view logic using the aggregated data
        # Example: self.dashboard_view.update(aggregated_data)

    except Exception as e:
        # Log error (replace 'print' with actual logging in a real-world application)
        print(f"Error updating dashboard view: {e}")
        # Handle error as needed, possibly raise for higher level handling

def get_migration_summary():
    """
    Prepares a summary of the migration data for display on the dashboard.
    
    Generates a summarized report based on the current migration data status.
    """
    try:
        # Check current migration status
        status = check_migration_status()
        if not status:
            raise ValueError("Migration status check failed.")

        # Prepare summary using fetched and aggregated data
        summary = {
            'status': status,
            # Further details could be added here based on fetched data
            # Ex: 'summary_data': fetch_migration_data(), etc.
        }

        return summary

    except Exception as e:
        # Log error (replace 'print' with actual logging in a real-world application)
        print(f"Error preparing migration summary: {e}")
        # Handle error, potentially return a fallback summary, or raise as required
        
        return {"status": "Error", "message": str(e)}
