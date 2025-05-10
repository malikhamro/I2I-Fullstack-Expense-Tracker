import json

# Simulated function; replace with actual import if modules exist
def check_role_validity(role):
    # Actual implementation should retrieve role validity and permissions
    return {
        "role": role,
        "valid": True,
        "permissions": ["read", "write", "delete"]
    }

def verify_user_role(user_id):
    """
    Verify which role a user is assigned to, and retrieve the role's permissions.

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        dict: Contains user_id, role, and permissions if the user and role are valid.
              Raises an appropriate error otherwise.
    """
    try:
        # Here, we simulate user-role retrieval; replace with actual database query
        # Example: user_role_data = db.query(UserRoles).filter_by(user_id=user_id).first()
        user_role_data = {
            "user_id": user_id,
            "role": "admin"  # Example role; replace with actual role retrieval logic
        }
        
        if not user_role_data:
            raise ValueError("User not found.")
        
        role = user_role_data["role"]
        
        role_data = check_role_validity(role)
        
        if not role_data["valid"]:
            raise ValueError("Invalid role assigned to the user.")
        
        return {
            "user_id": user_id,
            "role": role,
            "permissions": role_data["permissions"]
        }
    
    except Exception as e:
        # Log the error details appropriately
        # Example: logger.error(f"Error verifying user role: {e}")
        raise ValueError(f"Error verifying user role: {e}")

# Example usage:
if __name__ == "__main__":
    try:
        result = verify_user_role("user123")
        print(json.dumps(result, indent=2))
    except ValueError as e:
        print(e)
