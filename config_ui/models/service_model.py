# File: config_ui/models/service_model.py

from typing import Dict, Any

class Service:
    """
    Represents the service data model.
    """
    def __init__(self, id: int, name: str, url: str, timeout: int):
        self.id = id
        self.name = name
        self.url = url
        self.timeout = timeout

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Service':
        """
        Converts a dictionary to a Service object.

        Args:
            data (dict): A dictionary containing service data.

        Returns:
            Service: A Service object.
        """
        try:
            id = int(data.get('id'))
            name = str(data.get('name'))
            url = str(data.get('url'))
            timeout = int(data.get('timeout'))
            return Service(id=id, name=name, url=url, timeout=timeout)
        except (TypeError, ValueError, AttributeError) as e:
            raise ValueError('Invalid data structure for Service.') from e

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts a Service object to a dictionary.

        Returns:
            dict: A dictionary representation of the Service object.
        """
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'timeout': self.timeout,
        }
