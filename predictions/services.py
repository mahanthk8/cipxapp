from datetime import datetime
from users.models import User
from complaints.models import Complaint
from django.db.models import Count, Q

def detect_season():
    month = datetime.now().month

    if month in [6, 7, 8, 9]:  # Adjust for region
        return "Rainy"
    elif month in [10, 11, 12, 1]:
        return "Winter"
    else:
        return "Summer"


def predict_priority(description):
    description = description.lower()
    season = detect_season()

    high_keywords = ["overflow", "fire", "accident", "danger", "urgent"]
    mosquito_keywords = ["mosquito"]
    garbage_keywords = ["garbage", "waste"]
    drainage_keywords = ["drainage"]

    # Universal high
    for word in high_keywords:
        if word in description:
            return "HIGH"

    # Rainy amplification
    if season == "Rainy":
        if any(word in description for word in mosquito_keywords + drainage_keywords):
            return "HIGH"

    # Medium cases
    if any(word in description for word in garbage_keywords):
        return "MEDIUM"

    return "LOW"



def estimate_resolution_time(priority):
    if priority == "HIGH":
        return "24 Hours"
    elif priority == "MEDIUM":
        return "3 Days"
    return "7 Days"


def smart_officer_assignment(priority):
    officers = User.objects.filter(role='OFFICER')

    if not officers.exists():
        return None

    # Priority weights
    if priority == "HIGH":
        star_weight = 2.0
        workload_weight = 1.5
    elif priority == "MEDIUM":
        star_weight = 1.5
        workload_weight = 1.2
    else:
        star_weight = 1.0
        workload_weight = 1.0

    best_officer = None
    best_score = -9999

    for officer in officers:
        active_count = officer.assigned_complaints.filter(
            status__in=["PENDING", "IN_PROGRESS"]
        ).count()

        score = (star_weight * officer.star) - (workload_weight * active_count)

        if score > best_score:
            best_score = score
            best_officer = officer

    return best_officer
