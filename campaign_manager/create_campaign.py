# campaign_manager/create_campaign.py

import re
import json
from google.auth import exceptions as google_auth_exceptions
from google_ads_api_client import GoogleAdsApiClient, GoogleAdsApiException

def validate_campaign_data(campaign_data):
    """
    Validates the campaign data provided by the user. Checks for field completeness, data types, and value constraints.
    
    Parameters:
    campaign_data (dict): User input campaign data.
    
    Returns:
    bool: True if the data is valid, raises ValueError with an appropriate message if the data is invalid.
    """
    required_fields = {
        'name': str,
        'budget': (int, float),
        'start_date': str,
        'end_date': str,
        'ad_text': str,
        'keywords': list
    }
    
    for field, expected_type in required_fields.items():
        if field not in campaign_data:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(campaign_data[field], expected_type):
            raise ValueError(f"Incorrect type for field {field}: expected {expected_type}, got {type(campaign_data[field])}")
    
    if not re.match(r'\d{4}-\d{2}-\d{2}', campaign_data['start_date']):
        raise ValueError(f"Incorrect date format for start_date, expected YYYY-MM-DD")
    
    if not re.match(r'\d{4}-\d{2}-\d{2}', campaign_data['end_date']):
        raise ValueError(f"Incorrect date format for end_date, expected YYYY-MM-DD")

    if campaign_data['start_date'] >= campaign_data['end_date']:
        raise ValueError("start_date should be earlier than end_date")
    
    return True

def format_campaign_data(validated_data):
    """
    Formats the validated campaign data to match Google Ads API requirements.
    
    Parameters:
    validated_data (dict): The validated campaign data.
    
    Returns:
    dict: The formatted campaign data ready for API submission.
    """
    formatted_data = {
        'campaign': {
            'name': validated_data['name'],
            'advertising_channel_type': 'SEARCH',
            'status': 'PAUSED',
            'manual_cpc': {
                'enhanced_cpc_enabled': False,
            },
            'campaign_budget': {
                'amount_micros': int(validated_data['budget'] * 1e6),
            },
            'start_date': validated_data['start_date'].replace('-', ''),
            'end_date': validated_data['end_date'].replace('-', ''),
            'ad_group': [
                {
                    'name': f"{validated_data['name']} Ad Group",
                    'ad_group_ad': [
                        {
                            'ad': {
                                'expanded_text_ad': {
                                    'headline_part1': validated_data['ad_text'],
                                    'headline_part2': validated_data['ad_text'],
                                    'description': validated_data['ad_text'],
                                },
                            },
                        },
                    ],
                    'keywords': validated_data['keywords'],
                },
            ],
        },
    }
    
    return formatted_data

def send_campaign_to_google_ads(formatted_data):
    """
    Sends the formatted campaign data to Google Ads using the API.
    
    Parameters:
    formatted_data (dict): The formatted campaign data.
    
    Returns:
    dict: The API response containing the created campaign information.
    """
    try:
        client = GoogleAdsApiClient()
        response = client.create_campaign(formatted_data)
        return response
    except GoogleAdsApiException as e:
        raise RuntimeError(f"Google Ads API error: {e}")
    except google_auth_exceptions.GoogleAuthError as e:
        raise RuntimeError(f"Google authentication error: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")

def create_campaign(campaign_data):
    """
    Main function to create a Google Ads campaign. This function integrates the validation, formatting, and sending steps.
    
    Parameters:
    campaign_data (dict): User input campaign data.
    
    Returns:
    dict: Response from Google Ads API containing the created campaign information.
    """
    try:
        validate_campaign_data(campaign_data)
        formatted_data = format_campaign_data(campaign_data)
        response = send_campaign_to_google_ads(formatted_data)
        return response
    except ValueError as e:
        print(f"Validation error: {e}")
    except RuntimeError as e:
        print(f"Runtime error: {e}")
