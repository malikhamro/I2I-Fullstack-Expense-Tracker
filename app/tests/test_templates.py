import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Contributions


class ContributionsSummaryTemplateTestCase(TestCase):

    def setUp(self):
        # Setup test user and contributions
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        self.contributions_url = reverse('contributions_summary')

        # Create dummy contributions for the test user
        Contributions.objects.create(user=self.user, amount=1000.00, date='2023-01-01')
        Contributions.objects.create(user=self.user, amount=1500.00, date='2023-02-01')

    def test_contributions_summary_template(self):
        # Access the contributions summary page
        response = self.client.get(self.contributions_url)

        # Check that the request was successful
        self.assertEqual(response.status_code, 200)

        # Check that the template used is the correct one
        self.assertTemplateUsed(response, 'contributions_summary.html')

        # Verify the correct context data is passed to the template
        self.assertIn('total_contributions', response.context)
        self.assertEqual(response.context['total_contributions'], 2500.00)

        # Check that the rendered content contains the correct total contributions
        self.assertContains(response, 'Total Contributions: $2500.00')

    def tearDown(self):
        # Clean up after each test
        self.user.delete()
        Contributions.objects.all().delete()


if __name__ == "__main__":
    unittest.main()
