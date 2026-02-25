from django.urls import path
from . import views

urlpatterns = [

    path("user/",views.userDashboardView,name="user_dashboard"),
    path("admin/",views.adminDashboardView,name="admin_dashboard"),
    path("owner/",views.servicestaffDashboardView,name="servicestaff_dashboard"),
]