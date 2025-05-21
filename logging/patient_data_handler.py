import json
from datetime import datetime
from logging.modification_logger import log_modification

def update_patient_data(patient_data, updates, user_id):
    """
    This function will handle the updating of patient data.
    It ensures that before any changes are committed, the `log_modification`
    function is called to log the changes for compliance purposes.

    :param patient_data: dict, the original patient data
    :param updates: dict, the fields and values to update in the patient data
    :param user_id: str, ID of the user performing the update

    :return: dict, updated patient data
    """
    
    if not isinstance(patient_data, dict) or not isinstance(updates, dict):
        raise ValueError("Patient data and updates must be dictionaries.")

    if not user_id:
        raise ValueError("User ID must be provided.")

    modified_fields = {}
    original_data = patient_data.copy()

    try:
        for key, value in updates.items():
            if key in patient_data:
                if patient_data[key] != value:
                    modified_fields[key] = {"old": patient_data[key], "new": value}
                    patient_data[key] = value

        if modified_fields:
            log_modification(
                user_id=user_id,
                timestamp=datetime.utcnow().isoformat(),
                modified_fields=modified_fields,
                original_data=original_data,
                updated_data=patient_data
            )
    except Exception as e:
        # Log error or handle this
        raise RuntimeError(f"Failed to update patient data: {str(e)}")

    return patient_data
