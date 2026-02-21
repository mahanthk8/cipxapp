from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Complaint
from .forms import ComplaintForm, ComplaintAssignForm, OfficerUpdateForm
from users.decorators import role_required
from .services import auto_assign_complaint

def tracking_view(request):
    context = {}

    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        try:
            complaint = Complaint.objects.get(complaintId=complaint_id)
            context['complaint'] = complaint
        except Complaint.DoesNotExist:
            context['error'] = "Complaint not found."

    return render(request, "track.html", context)




@login_required
@role_required('USER')
def create_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.created_by = request.user
            complaint.action_by = request.user
            complaint.save()
            messages.success(request, "Complaint created successfully.")

            # AUTO ASSIGN
            auto_assign_complaint(complaint)

            return redirect('user_dashboard')
    else:
        form = ComplaintForm()

    return render(request, 'complaint/create.html', {'form': form})


@login_required
@role_required('USER')
def edit_complaint(request, complaint_id):
    complaint = get_object_or_404(
        Complaint,
        complaintId=complaint_id,
        created_by=request.user
    )

    if complaint.status != 'PENDING':
        messages.error(request, "Only pending complaints can be edited.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.action_by = request.user
            updated.save()
            messages.success(request, "Complaint updated successfully.")
            return redirect('user_dashboard')
    else:
        form = ComplaintForm(instance=complaint)

    return render(request, 'complaint/edit.html', {'form': form})


@login_required
@role_required('ADMIN')
def admin_assign_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)

    if request.method == 'POST':
        form = ComplaintAssignForm(request.POST, instance=complaint, region=complaint.region)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.action_by = request.user
            updated.save()
            messages.success(request, "Complaint assigned successfully.")
            return redirect('admin_complaint_list')
    else:
        form = ComplaintAssignForm(instance=complaint, region=complaint.region)

    return render(request, 'admin/assign_to_officer.html', {
        'form': form,
        'complaint': complaint
    })


# FILE: complaints/views.py

@login_required
@role_required('OFFICER')
def officer_update_complaint(request, pk):
    # Ensure officer can only edit their assigned complaints
    complaint = get_object_or_404(
        Complaint,
        pk=pk,
        assigned_to=request.user
    )

    if request.method == 'POST':
        form = OfficerUpdateForm(
            request.POST,
            request.FILES,
            instance=complaint
        )

        if form.is_valid():
            updated = form.save(commit=False)
            updated.action_by = request.user
            updated.save()
            
            # STAR LOGIC
            if updated.status == 'COMPLETED':
                request.user.star = min(request.user.star + 0.5, 100)
                request.user.save()

            messages.success(request, "Complaint updated successfully.")
            return redirect('officer_dashboard') # Moved inside the success block
        

    else:
        # This handles the INITIAL page load (GET request)
        form = OfficerUpdateForm(instance=complaint)

    # Now 'form' is guaranteed to exist for the render function
    return render(request, 'officer/officer_update_complaint.html', {
        'form': form,
        'complaint': complaint
    })


# FILE: complaints/views.py

from django.db.models import Q
from datetime import datetime
from regions.models import Region
from users.models import User


@login_required
@role_required('ADMIN')
def admin_complaint_list(request):

    complaints = Complaint.objects.select_related(
        'region', 'created_by', 'assigned_to'
    ).all()

    # --- Filters ---
    region = request.GET.get('region')
    status = request.GET.get('status')
    officer = request.GET.get('officer')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if region:
        complaints = complaints.filter(region__id=region)

    if status:
        complaints = complaints.filter(status=status)

    if officer:
        complaints = complaints.filter(assigned_to__id=officer)

    if start_date and end_date:
        complaints = complaints.filter(
            created_at__date__range=[start_date, end_date]
        )

    context = {
        'complaints': complaints,
        'regions': Region.objects.all(),
        'officers': User.objects.filter(role='OFFICER'),
    }

    return render(request, 'admin/complaint_list.html', context)



@login_required
def view_complaint(request, complaintId): 
    complaint = get_object_or_404(
        Complaint.objects.select_related(
            'region', 'created_by', 'assigned_to', 'action_by'
        ),
        # 2. Filter by the tracking field 'complaintId'
        complaintId=complaintId 
    )

    audit_logs = complaint.audit_logs.select_related(
        'changed_by'
    ).order_by('-timestamp')

    return render(request, 'complaint/complaint_detail.html', {
        'complaint': complaint,
        'audit_logs': audit_logs
    })



from django.db.models import Count
from django.db.models.functions import Coalesce
from django.db.models import Q

@login_required
@role_required('ADMIN')
def admin_dashboard_main_v2(request):

    total_complaints = Complaint.objects.count()

    # Complaints by Status
    status_data = (
        Complaint.objects
        .values('status')
        .annotate(count=Count('id'))
        .order_by()
    )

    # Complaints by Region
    region_data = (
        Complaint.objects
        .values('region__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Officer workload
    officer_data = (
        Complaint.objects
        .filter(assigned_to__isnull=False)
        .values('assigned_to__username')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    context = {
        'total_complaints': total_complaints,
        'status_data': list(status_data),
        'region_data': list(region_data),
        'officer_data': list(officer_data),
    }

    return render(request, 'admin/admin_dashboard_main_v2.html', context)
