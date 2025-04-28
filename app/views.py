# app/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .models import Contributions

def get_contributions_data(pension_holder_id):
    try:
        contributions = Contributions.objects.filter(pension_holder_id=pension_holder_id)
        total_contributions = sum(contribution.amount for contribution in contributions)
        return total_contributions, contributions
    except Contributions.DoesNotExist:
        return 0, []

def view_contributions_summary(request, pension_holder_id):
    try:
        total_contributions, contributions_list = get_contributions_data(pension_holder_id)
        context = {
            'total_contributions': total_contributions,
            'contributions_list': contributions_list,
            'pension_holder_id': pension_holder_id
        }
        return render(request, 'contributions_summary.html', context)
    except Exception as e:
        return HttpResponse(f"An error occurred while processing request: {e}", status=500)
