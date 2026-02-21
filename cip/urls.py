"""
URL configuration for cip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
# Consolidate imports: Import the views module once per app
from dashboard.views import dashboard_router
from users import views as user_views
from complaints import views as complaint_views

urlpatterns = [
    # Core Admin
    path('admin/', admin.site.urls),

    # General / Authentication
    path('', user_views.home, name='home'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('register/', user_views.register_view, name='register'),
    path('register/admin/', user_views.admin_register_view, name='admin_register'),

    # User Management
    path('user/dashboard/', user_views.user_dashboard, name='user_dashboard'),
    path('user/profile/', user_views.profile_update, name='profile_update'),

    # Complaints
    path('tracking/', complaint_views.tracking_view, name='tracking'),
    path('complaint/create/', complaint_views.create_complaint, name='create_complaint'),
    path('complaint/edit/<str:complaintId>/', complaint_views.edit_complaint, name='edit_complaint'),
    path('complaint/detail/<str:complaintId>/', complaint_views.view_complaint, name='view_complaint'),
    # Dashboard
    path('dashboard/', dashboard_router, name='dashboard_router'),

    # Officer Dashboard
    path('officer/dashboard/', user_views.officer_dashboard, name='officer_dashboard'),
    path('officer/complaint/update/<int:pk>/', complaint_views.officer_update_complaint, name='officer_update_complaint'),
]


from regions import views as region_views
from dashboard import views as dashboard_views


urlpatterns += [
    path('cip/admin/regions/', region_views.region_list, name='region_list'),
    path('cip/admin/regions/create/', region_views.region_create, name='region_create'),
    path('cip/admin/regions/update/<int:pk>/', region_views.region_update, name='region_update'),
    path('cip/admin/regions/delete/<int:pk>/', region_views.region_delete, name='region_delete'),
    path('cip/admin/officers/', user_views.officer_list, name='officer_list'),
    path('cip/admin/officers/create/', user_views.officer_create, name='officer_create'),
    path('cip/admin/officers/update/<int:pk>/', user_views.officer_update, name='officer_update'),
    path('cip/admin/officers/toggle-status/<int:pk>/', user_views.officer_toggle_status, name='officer_toggle_status'),
    path('cip/admin/complaints/', complaint_views.admin_complaint_list, name='admin_complaint_list'),
    path('cip/admin/complaints/assign/<int:pk>/', complaint_views.admin_assign_complaint, name='admin_assign'),
    path('cip/admin/dashboard/', dashboard_views.admin_dashboard_main, name='admin_dashboard_main'),
    path('cip/admin/dashboard/v2/', complaint_views.admin_dashboard_main_v2, name='admin_dashboard_main_v2'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
