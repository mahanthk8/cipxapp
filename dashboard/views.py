from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q
from users.decorators import role_required
from complaints.models import Complaint
from users.models import User
from regions.models import Region


@login_required
def dashboard_router(request):
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard_main')
    elif request.user.role == 'OFFICER':
        return redirect('officer_dashboard')
    else:
        return redirect('user_dashboard')


# FILE: dashboard/views.py

def admin_analytics(request):

    priority_stats = Complaint.objects.values('priority').annotate(
        total=Count('id')
    )

    season_stats = Complaint.objects.values('season_tag').annotate(
        total=Count('id')
    )

    officer_performance = User.objects.filter(role='OFFICER').annotate(
        completed_count=Count(
            'assigned_complaints',
            filter=Q(assigned_complaints__status="COMPLETED")
        )
    ).order_by('-star')

    context = {
        "priority_stats": priority_stats,
        "season_stats": season_stats,
        "officer_performance": officer_performance
    }

    return render(request, "admin/analytics.html", context)






@login_required
@role_required('ADMIN')
def admin_dashboard_main(request):

    # ---- KPI COUNTS ----
    total_complaints = Complaint.objects.count()
    pending_count = Complaint.objects.filter(status='PENDING').count()
    in_process_count = Complaint.objects.filter(status='IN_PROCESS').count()
    completed_count = Complaint.objects.filter(status='COMPLETED').count()
    rejected_count = Complaint.objects.filter(status='REJECTED').count()

    total_officers = User.objects.filter(role='OFFICER').count()
    total_regions = Region.objects.count()

    # ---- Complaints by Status ----
    status_data = (
        Complaint.objects
        .values('status')
        .annotate(count=Count('id'))
    )

    status_labels = [item['status'] for item in status_data]
    status_counts = [item['count'] for item in status_data]

    # ---- Complaints by Region ----
    region_data = (
        Complaint.objects
        .values('region__name')
        .annotate(count=Count('id'))
    )

    region_labels = [item['region__name'] for item in region_data]
    region_counts = [item['count'] for item in region_data]

    
    from django.db.models import Count as dcount, Case, When, IntegerField
    officer_data = User.objects.filter(role='OFFICER').annotate(
    workload=dcount(
            Case(
                When(assigned_complaints__status='PENDING', then=1),
                output_field=IntegerField(),
            )
        )
    )

    priority_stats = Complaint.objects.values('priority').annotate(
        total=Count('id')
    )

    season_stats = Complaint.objects.values('season_tag').annotate(
        total=Count('id')
    )

    officer_performance = User.objects.filter(role='OFFICER').annotate(
        completed_count=Count(
            'assigned_complaints',
            filter=Q(assigned_complaints__status="COMPLETED")
        )
    ).order_by('-star')

    officer_labels = [o.username for o in officer_data]
    officer_counts = [o.assigned_complaints.count() for o in officer_data]

    context = {
        'total_complaints': total_complaints,
        'pending_count': pending_count,
        'in_process_count': in_process_count,
        'completed_count': completed_count,
        'rejected_count': rejected_count,
        'total_officers': total_officers,
        'total_regions': total_regions,

        'status_labels': status_labels,
        'status_counts': status_counts,

        'region_labels': region_labels,
        'region_counts': region_counts,

        'officer_labels': officer_labels,
        'officer_counts': officer_counts,
        "priority_stats": priority_stats,
        "season_stats": season_stats,
        "officer_performance": officer_performance
    }

    return render(request, 'admin/admin_dashboard_main.html', context)
