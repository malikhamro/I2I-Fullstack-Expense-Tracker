# src/update_claim_status.py

from database import update_claim_status_in_db, get_claim_by_id
from notifications import notify_stakeholders

class InvalidClaimIDException(Exception):
    pass

class DatabaseUpdateException(Exception):
    pass

def update_claim_status(claim_id, new_status, remarks=None):
    """
    Enables a claims processor to update the status of insurance claims. It takes the claim ID, new status, 
    and optional remarks as inputs, and updates the status in the database. Additionally, it triggers 
    notifications to stakeholders about the status update. Uses notify_stakeholders function from 
    notifications.py to send notifications.

    :param claim_id: int - The ID of the claim to update
    :param new_status: str - The new status for the claim
    :param remarks: str - Optional remarks about the status update
    :raises InvalidClaimIDException: If the claim ID does not exist
    :raises DatabaseUpdateException: If updating the claim in the database fails
    """
    try:
        # Retrieve current claim details
        claim_details = get_claim_by_id(claim_id)
        if not claim_details:
            raise InvalidClaimIDException(f"No claim found with ID {claim_id}")

        # Update the claim status in the database
        update_result = update_claim_status_in_db(claim_id, new_status)
        if not update_result:
            raise DatabaseUpdateException(f"Failed to update claim status for ID {claim_id}")

        # Trigger notifications to stakeholders
        notify_stakeholders(claim_details, new_status, remarks)
        print(f"Claim ID {claim_id} status successfully updated to {new_status}")

    except InvalidClaimIDException as e:
        print(f"Error: {str(e)}")
        raise

    except DatabaseUpdateException as e:
        print(f"Error: {str(e)}")
        raise

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        raise
