from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from users.decorators import role_required
from .forms import AdminRegisterForm, UserRegisterForm, UserUpdateForm, OfficerCreateForm
from complaints.models import Complaint

def home(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def admin_register_view(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Admin registration successful.")
            return redirect('login')
    else:
        form = AdminRegisterForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard_router')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def user_dashboard(request):
    complaints = Complaint.objects.filter(created_by=request.user)

    return render(request, 'user/user_dashboard.html', {'complaints': complaints})



@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_dashboard')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'user/user_profile.html', {'form': form})

# < -- offier views -- >

from django.db.models import Count, Q

@login_required
@role_required('OFFICER')
def officer_dashboard(request):
    complaints = request.user.assigned_complaints.all()
    context = {"complaints": complaints}
    return render(request, 'officer/officer_dashboard.html', context)


# < -- Admin Views for Officer Management -->

@login_required
@role_required('ADMIN')
def officer_list(request):
    User = get_user_model()
    officers = User.objects.filter(role='OFFICER')
    active_counts = {}
    for officer in officers:
        active_counts[officer.id] = officer.assigned_complaints.filter(
            status__in=["PENDING", "IN_PROCESS"]
        ).count()
    for officer in officers:
        officer.active_cases = active_counts.get(officer.id, 0)
    return render(request, 'admin/officer_list.html', {'officers': officers, 'active_counts': active_counts})


@login_required
@role_required('ADMIN')
def officer_create(request):
    if request.method == 'POST':
        form = OfficerCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('officer_list')
    else:
        form = OfficerCreateForm()

    return render(request, 'admin/officer_create.html', {'form': form})

@login_required
@role_required('ADMIN')
def officer_update(request, pk):
    User = get_user_model()
    officer = User.objects.get(pk=pk, role='OFFICER')
    if request.method == 'POST':
        form = OfficerCreateForm(request.POST, instance=officer)
        if form.is_valid():
            form.save()
            return redirect('officer_list')
    else:
        form = OfficerCreateForm(instance=officer)

    return render(request, 'admin/officer_update.html', {'form': form})


@login_required
@role_required('ADMIN')
def officer_toggle_status(request, pk):
    User = get_user_model()
    officer = User.objects.get(pk=pk, role='OFFICER')
    officer.is_active = not officer.is_active
    officer.save()
    return redirect('officer_list')




