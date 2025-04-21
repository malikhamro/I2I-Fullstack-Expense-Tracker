# config_ui/services/policy_service.py

from config_ui.models.policy_model import Policy, from_dict, to_dict
from config_ui.controllers.policy_controller import get_policies, add_policy, update_policy, delete_policy


def list_policies():
    """
    Business logic for listing policies.
    Retrieves the list of policies by calling the appropriate controller function.
    """
    try:
        # Assuming `get_policies` returns a list of policy dictionaries
        policies = get_policies()
        return [to_dict(policy) for policy in policies]
    except Exception as e:
        # Log the exception and re-raise or handle it accordingly
        # For simplicity's sake, we re-raise the exception here.
        raise RuntimeError(f"Failed to list policies: {str(e)}")


def create_policy(policy_data):
    """
    Business logic for creating a new policy.
    Uses the provided policy data to create a new policy object and store it.

    :param policy_data: Dictionary containing policy data
    :return: The created policy as a dictionary
    """
    try:
        policy = from_dict(policy_data)
        add_policy(policy)
        return to_dict(policy)
    except ValueError as e:
        raise ValueError(f"Invalid policy data: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to create policy: {str(e)}")


def edit_policy(policy_id, policy_data):
    """
    Business logic for editing an existing policy.
    Uses the policy_id to find and update the policy with the new data.

    :param policy_id: ID of the policy to edit
    :param policy_data: Dictionary containing the new policy data
    :return: The updated policy as a dictionary
    """
    try:
        # Validate the policy ID and data
        if not policy_id or not policy_data:
            raise ValueError("Policy ID and data must be provided")

        updated_policy_data = from_dict(policy_data)
        update_policy(policy_id, updated_policy_data)
        return to_dict(updated_policy_data)
    except ValueError as e:
        raise ValueError(f"Invalid policy data or ID: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to edit policy: {str(e)}")


def remove_policy(policy_id):
    """
    Business logic for removing a policy.
    Uses the policy_id to find and delete the policy.

    :param policy_id: ID of the policy to remove
    """
    try:
        if not policy_id:
            raise ValueError("Policy ID must be provided")
        
        delete_policy(policy_id)
    except ValueError as e:
        raise ValueError(f"Invalid policy ID: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to remove policy: {str(e)}")
