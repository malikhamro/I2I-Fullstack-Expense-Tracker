# data_consistency/policy_storage.py

import json
import os
from typing import Dict, Any

POLICY_STORAGE_FILE = 'data_consistency_policies.json'

def store_policy(policy: Dict[str, Any]) -> None:
    """
    Stores the defined data consistency policies in a persistent storage system.
    
    Args:
        policy (Dict[str, Any]): A dictionary containing the data consistency policies.
    
    Raises:
        ValueError: If the policy is not a dictionary.
        IOError: If there is an issue writing to the storage file.
    """
    if not isinstance(policy, Dict):
        raise ValueError("Policy must be a dictionary")

    try:
        with open(POLICY_STORAGE_FILE, 'w') as file:
            json.dump(policy, file, indent=4)
    except IOError as e:
        raise IOError(f"Error storing policy: {e}")

def retrieve_policy() -> Dict[str, Any]:
    """
    Retrieves the stored data consistency policies for validation and monitoring purposes.
    
    Returns:
        Dict[str, Any]: A dictionary containing the data consistency policies.
    
    Raises:
        IOError: If there is an issue reading from the storage file.
        FileNotFoundError: If the storage file does not exist.
        ValueError: If the content of the storage file is not a valid JSON.
    """
    if not os.path.exists(POLICY_STORAGE_FILE):
        raise FileNotFoundError(f"{POLICY_STORAGE_FILE} does not exist")

    try:
        with open(POLICY_STORAGE_FILE, 'r') as file:
            policy = json.load(file)
    except IOError as e:
        raise IOError(f"Error retrieving policy: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid JSON format in policy storage: {e}")

    return policy

def update_policy(new_policy: Dict[str, Any]) -> None:
    """
    Updates the stored policies based on new rules defined or modifications in the existing ones.
    
    Args:
        new_policy (Dict[str, Any]): A dictionary containing the updated data consistency policies.
    
    Raises:
        ValueError: If the new policy is not a dictionary.
        IOError: If there is an issue writing to the storage file.
    """
    if not isinstance(new_policy, Dict):
        raise ValueError("New policy must be a dictionary")

    try:
        with open(POLICY_STORAGE_FILE, 'w') as file:
            json.dump(new_policy, file, indent=4)
    except IOError as e:
        raise IOError(f"Error updating policy: {e}")
