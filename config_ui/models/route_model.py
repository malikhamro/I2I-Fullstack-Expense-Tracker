# config_ui/models/route_model.py

class Route:
    def __init__(self, id, path, method, service_id):
        """
        Represents the route data model.

        :param id: Unique identifier for the route.
        :param path: URL path for the route.
        :param method: HTTP method used by the route (e.g., GET, POST).
        :param service_id: Identifier of the service associated with the route.
        """
        self.id = id
        self.path = path
        self.method = method
        self.service_id = service_id

    def to_dict(self):
        """
        Converts a Route object to a dictionary.

        :return: Dictionary representation of the Route object.
        """
        return {
            'id': self.id,
            'path': self.path,
            'method': self.method,
            'service_id': self.service_id
        }

    @staticmethod
    def from_dict(data):
        """
        Converts a dictionary to a Route object.

        :param data: Data dictionary containing route details.
        :return: New Route object.
        :raises ValueError: If the provided data is invalid.
        """
        try:
            return Route(
                id=data['id'],
                path=data['path'],
                method=data['method'],
                service_id=data['service_id']
            )
        except KeyError as e:
            raise ValueError(f'Missing required field in data: {e}')
        except TypeError:
            raise ValueError(f'Invalid data type for Route creation')
