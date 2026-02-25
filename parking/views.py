from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="login") #check in core.urls.py login name should exist..
def adminDashboardView(request):
    return render(request,"parking/admin_dashboard.html")

@login_required(login_url="login")
def userDashboardView(request):
    return render(request,"parking/user_dashboard.html")

@login_required(login_url="login") #check in core.urls.py login name should exist..
def servicestaffDashboardView(request):
    return render(request,"parking/servicestaff_dashboard.html")