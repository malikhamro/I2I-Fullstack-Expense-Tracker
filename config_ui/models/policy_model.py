# config_ui/models/policy_model.py

from typing import Optional

class Policy:
    def __init__(self, policy_id: Optional[int] = None, name: str = "", rules: Optional[dict] = None):
        self.policy_id = policy_id
        self.name = name
        self.rules = rules if rules is not None else {}

    @staticmethod
    def from_dict(data: dict) -> "Policy":
        if not isinstance(data, dict):
            raise ValueError("Input should be a dictionary")
        
        policy_id = data.get('policy_id')
        name = data.get('name')
        rules = data.get('rules', {})

        if name is None:
            raise ValueError("Policy 'name' is required")

        return Policy(policy_id=policy_id, name=name, rules=rules)
    
    def to_dict(self) -> dict:
        return {
            'policy_id': self.policy_id,
            'name': self.name,
            'rules': self.rules,
        }
