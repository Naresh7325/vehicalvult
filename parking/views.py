from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import Vehicle , Documentation , ServiceDetail , Transportation , ParkingDetails 
from .forms import VehicleForm , DocumentForm , ServiceForm , TransportForm , ParkingForm

# Create your views here.
@login_required(login_url="login") #check in core.urls.py login name should exist..
def adminDashboardView(request):
    return render(request,"dashboard/admin_dashboard.html")

@login_required(login_url="login")
def userDashboardView(request):
    return render(request,"dashboard/user_dashboard.html")

@login_required(login_url="login") #check in core.urls.py login name should exist..
def servicestaffDashboardView(request):
    return render(request,"dashboard/servicestaff_dashboard.html")

def vehicle_list(request):

    vehicles = Vehicle.objects.filter(userId=request.user)

    return render(request,'vehicle/vehicle_list.html',{
        'vehicles':vehicles
    })


def add_vehicle(request):

    form = VehicleForm()

    if request.method == "POST":

        form = VehicleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('vehicle_list')

    return render(request,'vehicle/add_vehicle.html',{
        'form':form
    })

def upload_document(request):

    form = DocumentForm()

    if request.method == "POST":

        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('document_list')

    return render(request,'documents/upload_document.html',{
        'form':form
    })


def document_list(request):

    docs = Documentation.objects.all()

    return render(request,'documents/document_list.html',{
        'docs':docs
    })


def add_service(request):

    form = ServiceForm()

    if request.method == "POST":

        form = ServiceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('service_list')

    return render(request,'service/add_service.html',{
        'form':form
    })


def service_list(request):

    services = ServiceDetail.objects.all()

    return render(request,'service/service_list.html',{
        'services':services
    })

def add_transport(request):

    form = TransportForm()

    if request.method == "POST":

        form = TransportForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('transport_list')

    return render(request,'transport/add_transport.html',{
        'form':form
    })


def transport_list(request):

    transports = Transportation.objects.all()

    return render(request,'transport/transport_list.html',{
        'transports':transports
    })

def parking_list(request):

    parking = ParkingDetails.objects.all()

    return render(request, "parking/parking_list.html", {"parking": parking})


def parking_entry(request):

    if request.method == "POST":

        form = ParkingForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("parking_list")

    else:

        form = ParkingForm()

    return render(request, "parking/parking_entry.html", {"form": form})