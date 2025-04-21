import logging
from dashboard.services.data_service import fetch_migration_data, aggregate_migration_data
from dashboard.services.status_service import check_migration_status
from dashboard.controllers.dashboard_controller import update_dashboard_view, get_migration_summary

def create_dashboard():
    """
    Initializes the creation of a monitoring dashboard for the migration process.
    This function fetches migration data, checks the migration status, aggregates the data,
    and then updates the dashboard view.
    
    Raises:
        Exception: If there is any error during the dashboard creation process.
    """
    try:
        # Fetch raw migration data
        migration_data = fetch_migration_data()
        if not migration_data:
            raise ValueError("No migration data retrieved.")
        
        # Check the current status of the migration process
        migration_status = check_migration_status()
        if not migration_status:
            raise ValueError("Failed to verify migration status.")
        
        # Aggregate the raw migration data for dashboard view
        aggregated_data = aggregate_migration_data(migration_data)
        if not aggregated_data:
            raise ValueError("Failed to aggregate migration data.")
        
        # Prepare the migration summary
        migration_summary = get_migration_summary(aggregated_data)
        if not migration_summary:
            raise ValueError("Failed to prepare migration summary.")
        
        # Update the dashboard with the aggregated data and summary
        update_dashboard_view(aggregated_data, migration_summary)
    
    except ValueError as ve:
        logging.error(f"ValueError occurred during dashboard creation: {ve}")
        raise
    except Exception as ex:
        logging.error(f"An error occurred during dashboard creation: {ex}")
        raise
