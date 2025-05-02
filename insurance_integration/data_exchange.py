# insurance_integration/data_exchange.py

import json
import logging
from datetime import datetime

class DataExchange:
    def __init__(self):
        self.logger = logging.getLogger('DataExchangeLogger')
        handler = logging.FileHandler('data_exchange.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def convert_to_provider_format(self, internal_data, provider_name):
        """
        Converts internal data format to the format required by the specified provider.

        Args:
            internal_data (dict): The internal data to be converted.
            provider_name (str): The name of the insurance provider for which the data needs to be formatted.

        Returns:
            dict: The data formatted according to the provider's specifications.
        
        Raises:
            ValueError: If the provider_name is not recognized.
        """
        provider_formats = {
            'ProviderA': self._convert_for_provider_a,
            'ProviderB': self._convert_for_provider_b,
            # Add more providers as necessary
        }

        if provider_name not in provider_formats:
            raise ValueError(f"Unrecognized provider name: {provider_name}")

        formatted_data = provider_formats[provider_name](internal_data)
        self.log_data_exchange('convert_to_provider_format', provider_name, formatted_data)

        return formatted_data

    def _convert_for_provider_a(self, internal_data):
        # Conversion logic specific to ProviderA
        return {
            "name": f"{internal_data['first_name']} {internal_data['last_name']}",
            "dob": internal_data["date_of_birth"],
            "policy_number": internal_data["policy_id"],
            # Add more field mapping as required
        }

    def _convert_for_provider_b(self, internal_data):
        # Conversion logic specific to ProviderB
        return {
            "full_name": f"{internal_data['first_name']} {internal_data['last_name']}",
            "birthdate": internal_data["date_of_birth"],
            "policy_no": internal_data["policy_id"],
            # Add more field mapping as required
        }

    def log_data_exchange(self, operation, provider_name, data):
        """
        Logs data exchange details for auditing and troubleshooting purposes.

        Args:
            operation (str): The name of the operation performed.
            provider_name (str): The name of the provider involved in the data exchange.
            data (dict): The data being logged.

        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "provider_name": provider_name,
            "data": data
        }
        self.logger.info(json.dumps(log_entry))

# Example usage:
# exchanger = DataExchange()
# formatted_data = exchanger.convert_to_provider_format(internal_data, 'ProviderA')
