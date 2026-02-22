# FILE: complaints/services.py

from django.db.models import Count
from users.models import User
from .models import Complaint
from django.db import models


def auto_assign_complaint(complaint):
    """
    Assign complaint to lowest workload officer in same region.
    """

    officers = User.objects.filter(
        role='OFFICER',
        region=complaint.region,
        is_active=True
    ).annotate(
        active_cases=Count('assigned_complaints', filter=models.Q(assigned_complaints__status__in=['PENDING', 'IN_PROCESS']))
    ).order_by('active_cases')

    if officers.exists():
        officer = officers.first()
        complaint.assigned_to = officer
        complaint.status = 'IN_PROCESS'
        complaint.action_by = officer
        complaint.save()
        return officer

    return None


from ml_engine.services import (
    predict_priority,
    predict_resolution
)
from django.utils import timezone


def enrich_complaint_with_ai(complaint):
    """
    Auto-assign ML predictions to complaint
    """

    data_dict = {
        "category": complaint.category,
        "region": complaint.region.name if complaint.region else None,
        "month": timezone.now().month,
        "day_of_week": timezone.now().weekday(),
        "is_weekend": 1 if timezone.now().weekday() >= 5 else 0,
    }

    # Predict
    # complaint.predicted_priority = predict_priority(data_dict)
    # complaint.predicted_resolution = predict_resolution(data_dict)
    pp = predict_priority(data_dict)
    pr = predict_resolution(data_dict)

    # complaint.save()
    print(f"ML Predicted Priority: {pp}, ML Predicted Resolution: {pr}")    
