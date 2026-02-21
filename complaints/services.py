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
