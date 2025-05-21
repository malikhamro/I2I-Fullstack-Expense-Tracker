import logging
from datetime import datetime

# Configure the logging system
logging.basicConfig(filename='patient_data_modifications.log', 
                    level=logging.INFO,
                    format='%(asctime)s - %(user_id)s - %(message)s')

def log_modification(user_id, patient_id, modified_fields):
    """
    Log detailed information about modifications made to patient data.

    This function logs the information about which user modified the patient data,
    the timestamp of modification, the fields that were modified, and their old 
    and new values.

    :param user_id: str, ID of the user who made the modification
    :param patient_id: str, ID of the patient whose data was modified
    :param modified_fields: dict, a dictionary containing the names of the modified fields as keys and 
                            tuples of (old_value, new_value) as values.
                            Example: {'first_name': ('John', 'Jonathan'), 'last_name': ('Doe', 'Smith')}

    :return: None
    """
    try:
        timestamp = datetime.now().isoformat()
        log_entries = []
        
        for field, (old_value, new_value) in modified_fields.items():
            log_entries.append(f"Field: {field}, Old Value: {old_value}, New Value: {new_value}")
        
        log_message = (f"UserID: {user_id}, PatientID: {patient_id}, "
                       f"Timestamp: {timestamp}, Modifications: {', '.join(log_entries)}")

        extra = {'user_id': user_id}
        logging.info(log_message, extra=extra)

    except Exception as e:
        logging.error(f"Failed to log modification: {str(e)}")

