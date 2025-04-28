import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from app.models import Contributions

@pytest.mark.django_db
def test_view_contributions_summary():
    # Create a test user
    user = User.objects.create_user(username='testuser', password='testpassword')
    
    # Create test contributions
    contribution1 = Contributions.objects.create(user=user, amount=100, date='2023-01-01')
    contribution2 = Contributions.objects.create(user=user, amount=150, date='2023-02-01')
    
    # Login the test user
    client = Client()
    client.login(username='testuser', password='testpassword')
    
    # Access the contributions summary view
    response = client.get(reverse('view_contributions_summary'))
    
    # Validate the response
    assert response.status_code == 200
    assert 'contributions_summary.html' in (t.name for t in response.templates)
    assert 'total_contributions' in response.context
    assert response.context['total_contributions'] == sum([contribution1.amount, contribution2.amount])

    # Check that the rendered content includes total contributions
    rendered_content = response.content.decode(response.charset)
    assert str(contribution1.amount) in rendered_content
    assert str(contribution2.amount) in rendered_content

# Ensure proper setup and teardown by using pytest fixtures if more complex setup is necessary
@pytest.fixture
def create_test_data(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    Contributions.objects.create(user=user, amount=100, date='2023-01-01')
    Contributions.objects.create(user=user, amount=150, date='2023-02-01')
    return user

def test_view_contributions_summary_with_fixture(create_test_data):
    user = create_test_data
    
    # Login the test user
    client = Client()
    client.login(username='testuser', password='testpassword')
    
    # Access the contributions summary view
    response = client.get(reverse('view_contributions_summary'))
    
    # Validate the response
    assert response.status_code == 200
    assert 'contributions_summary.html' in (t.name for t in response.templates)
    assert 'total_contributions' in response.context

    # Check the rendered content
    rendered_content = response.content.decode(response.charset)
    contributions = Contributions.objects.filter(user=user)
    total_contributions = sum(c.amount for c in contributions)
    assert str(total_contributions) in rendered_content
