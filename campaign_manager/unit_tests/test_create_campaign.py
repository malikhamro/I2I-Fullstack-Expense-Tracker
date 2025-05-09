import unittest
from unittest.mock import patch, Mock

# Assuming the functions to be tested are imported from create_campaign.py
from campaign_manager.create_campaign import validate_campaign_data, format_campaign_data, send_campaign_to_google_ads, create_campaign

class TestCreateCampaign(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.valid_campaign_data = {
            "name": "Test Campaign",
            "budget": 1000,
            "start_date": "2023-10-01",
            "end_date": "2023-12-31",
            "targeting": {
                "location": "USA",
                "languages": ["en"]
            }
        }

        self.invalid_campaign_data = {
            "name": "",
            "budget": -100,
            "start_date": "invalid-date",
            "end_date": "2023-12-31",
            "targeting": {
                "location": "USA",
                "languages": ["en"]
            }
        }

    @patch('campaign_manager.create_campaign.validate_campaign_data')
    def test_validate_campaign_data(self, mock_validate):
        # Test valid data
        mock_validate.return_value = True
        self.assertTrue(validate_campaign_data(self.valid_campaign_data))

        # Test invalid data
        mock_validate.return_value = False
        self.assertFalse(validate_campaign_data(self.invalid_campaign_data))

    @patch('campaign_manager.create_campaign.format_campaign_data')
    def test_format_campaign_data(self, mock_format):
        # Expected formatted data
        expected_format = {
            "campaignName": "Test Campaign",
            "campaignBudget": 1000,
            "campaignStartDate": "2023-10-01",
            "campaignEndDate": "2023-12-31",
            "campaignTargeting": {
                "geoTargeting": "USA",
                "languageTargeting": ["en"]
            }
        }

        mock_format.return_value = expected_format
        formatted_data = format_campaign_data(self.valid_campaign_data)
        
        self.assertEqual(formatted_data, expected_format)

    @patch('campaign_manager.create_campaign.google_ads_client')
    @patch('campaign_manager.create_campaign.send_campaign_to_google_ads')
    def test_send_campaign_to_google_ads(self, mock_send, mock_google_ads_client):
        # Mocking the Google Ads client's response
        mock_google_ads_client.return_value = Mock()
        mock_google_ads_client.return_value.create_campaign.return_value = {"status": "success"}

        # Test sending valid data
        mock_send.return_value = {"status": "success"}
        response = send_campaign_to_google_ads(self.valid_campaign_data)
        
        self.assertEqual(response, {"status": "success"})

    @patch('campaign_manager.create_campaign.validate_campaign_data')
    @patch('campaign_manager.create_campaign.format_campaign_data')
    @patch('campaign_manager.create_campaign.send_campaign_to_google_ads')
    def test_create_campaign(self, mock_validate, mock_format, mock_send):
        # Setup mocks
        mock_validate.return_value = True
        mock_format.return_value = {
            "campaignName": "Test Campaign",
            "campaignBudget": 1000,
            "campaignStartDate": "2023-10-01",
            "campaignEndDate": "2023-12-31",
            "campaignTargeting": {
                "geoTargeting": "USA",
                "languageTargeting": ["en"]
            }
        }
        mock_send.return_value = {"status": "success"}

        # Test campaign creation
        result = create_campaign(self.valid_campaign_data)
        
        self.assertEqual(result, {"status": "success"})
        mock_validate.assert_called_once_with(self.valid_campaign_data)
        mock_format.assert_called_once_with(self.valid_campaign_data)
        mock_send.assert_called_once_with(mock_format.return_value)

if __name__ == '__main__':
    unittest.main()
