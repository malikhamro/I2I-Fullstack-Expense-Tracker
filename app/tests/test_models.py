import unittest
from django.test import TestCase
from app.models import Contributions

class ContributionsModelTest(TestCase):
    def setUp(self):
        self.contribution1 = Contributions.objects.create(
            user_id=1,
            amount=100.0,
            date='2023-01-01'
        )
        self.contribution2 = Contributions.objects.create(
            user_id=1,
            amount=200.0,
            date='2023-02-01'
        )

    def test_contributions_creation(self):
        self.assertTrue(isinstance(self.contribution1, Contributions))
        self.assertTrue(isinstance(self.contribution2, Contributions))
        self.assertEqual(self.contribution1.amount, 100.0)
        self.assertEqual(self.contribution2.amount, 200.0)

    def test_contributions_sum(self):
        user_contributions = Contributions.objects.filter(user_id=1)
        total_contributions = sum(contribution.amount for contribution in user_contributions)
        self.assertEqual(total_contributions, 300.0)

    def test_contributions_str(self):
        self.assertEqual(str(self.contribution1), 'Contribution of 100.0 on 2023-01-01')
        self.assertEqual(str(self.contribution2), 'Contribution of 200.0 on 2023-02-01')

    def test_invalid_contribution(self):
        with self.assertRaises(ValueError):
            Contributions.objects.create(
                user_id=1,
                amount=-100.0,  # Invalid negative amount
                date='2023-03-01'
            )
