
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vehicle, Documentation, ServiceDetail, Transportation, ParkingDetails
from .forms import VehicleForm, DocumentForm, ServiceForm, TransportForm, ParkingForm
from core.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from core.models import User


def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
            user.password = make_password(new_password)  # 🔐 hash password
            user.save()

            messages.success(request, "Password updated successfully!")
            return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "User not found!")

    return render(request, "auth/forgot_password.html")
# ---------------- DASHBOARD ----------------
@login_required(login_url="login")
def dashboard(request):
    role = request.user.role

    context = {
        "role": role,
        "user": request.user
    }

    # ADMIN
    if role == "admin":
        context.update({
            "vehicles": Vehicle.objects.all(),
            "total_users": User.objects.count(),
            "total_vehicles": Vehicle.objects.count(),
            "total_services": ServiceDetail.objects.count(),
            "total_transport": Transportation.objects.count(),
        })

    # USER
    else:
        context.update({
            "vehicles": Vehicle.objects.filter(userId=request.user),
            "services": ServiceDetail.objects.filter(vehicleId__userId=request.user),
            "transports": Transportation.objects.filter(vehicleId__userId=request.user),
        })

    return render(request, "dashboard/dashboard.html", context)


# ---------------- VEHICLE ----------------
@login_required(login_url="login")
def vehicle_list(request):
    if request.user.role == "admin":
        vehicles = Vehicle.objects.all()
    else:
        vehicles = Vehicle.objects.filter(userId=request.user)

    return render(request, 'vehicle/vehicle_list.html', {'vehicles': vehicles})


@login_required(login_url="login")
def add_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.userId = request.user
            vehicle.save()
            return redirect("vehicle_list")
    else:
        form = VehicleForm()

    return render(request, 'vehicle/add_vehicle.html', {'form': form})


# ---------------- DOCUMENT ----------------
@login_required(login_url="login")
def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm()

    return render(request, 'documents/upload_document.html', {'form': form})


@login_required(login_url="login")
def document_list(request):
    if request.user.role == "admin":
        docs = Documentation.objects.all()
    else:
        docs = Documentation.objects.filter(vehicleId__userId=request.user)

    return render(request, 'documents/document_list.html', {'docs': docs})


# ---------------- SERVICE ----------------
@login_required(login_url="login")
def add_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        form.fields['vehicleId'].queryset = Vehicle.objects.filter(userId=request.user)

        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
        form.fields['vehicleId'].queryset = Vehicle.objects.filter(userId=request.user)

    return render(request, 'service/add_service.html', {'form': form})


@login_required(login_url="login")
def service_list(request):
    if request.user.role == "admin":
        services = ServiceDetail.objects.all()
    else:
        services = ServiceDetail.objects.filter(vehicleId__userId=request.user)

    return render(request, 'service/service_list.html', {'services': services})


# ✅ ADMIN ONLY STATUS UPDATE
@login_required(login_url="login")
def update_service(request, id):
    service = get_object_or_404(ServiceDetail, id=id)

    if request.user.role != "admin":
        return redirect("service_list")

    if request.method == "POST":
        new_status = request.POST.get("status")
        service.status = new_status
        service.save()
        return redirect("service_list")

    return render(request, "service/update_service.html", {"service": service})


@login_required(login_url="login")
def delete_service(request, id):
    service = get_object_or_404(ServiceDetail, id=id)

    if request.user.role != "admin":
        return redirect("service_list")

    service.delete()
    return redirect("service_list")


# ---------------- TRANSPORT ----------------
@login_required(login_url="login")
def add_transport(request):
    if request.method == "POST":
        form = TransportForm(request.POST)
        if form.is_valid():
            transport = form.save(commit=False)
            transport.save()
            return redirect("transport_list")
    else:
        form = TransportForm()
        form.fields['vehicleId'].queryset = Vehicle.objects.filter(userId=request.user)

    return render(request, "transport/add_transport.html", {"form": form})


@login_required(login_url="login")
def transport_list(request):
    if request.user.role == "admin":
        transports = Transportation.objects.all()
    else:
        transports = Transportation.objects.filter(vehicleId__userId=request.user)

    return render(request, "transport/transport_list.html", {"transports": transports})


@login_required(login_url="login")
def update_transport(request, id):
    transport = get_object_or_404(Transportation, id=id)

    if request.user.role != "admin":
        return redirect("transport_list")

    if request.method == "POST":
        form = TransportForm(request.POST, instance=transport)

        # ✅ IMPORTANT LINE (fix dropdown)
        form.fields['vehicleId'].queryset = Vehicle.objects.all()

        if form.is_valid():
            form.save()
            return redirect("transport_list")

    else:
        form = TransportForm(instance=transport)

        # ✅ IMPORTANT LINE (fix dropdown)
        form.fields['vehicleId'].queryset = Vehicle.objects.all()

    return render(request, "transport/update_transport.html", {"form": form})

@login_required(login_url="login")
def delete_transport(request, id):
    transport = get_object_or_404(Transportation, id=id)

    if request.user.role != "admin":
        return redirect("transport_list")

    transport.delete()
    return redirect("transport_list")



# ---------------- PARKING ----------------

@login_required(login_url="login")
def parking_list(request):
    parking = ParkingDetails.objects.all()
    return render(request, "parking/parking_list.html", {"parking": parking})


@login_required(login_url="login")
def parking_entry(request):
    if request.method == "POST":
        form = ParkingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("parking_list")
    else:
        form = ParkingForm()

    return render(request, "parking/parking_entry.html", {"form": form})


@login_required(login_url="login")
def delete_parking(request, id):
    parking = get_object_or_404(ParkingDetails, id=id)

    if request.user.role == "admin" or parking.vehicleId.userId == request.user:
        parking.delete()

    return redirect("parking_list")


# ---------------- ADMIN ONLY ----------------
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.role != "admin":
            return redirect("dashboard")

        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def manage_users(request):
    users = User.objects.all()
    return render(request, "dashboard/manage_users.html", {"users": users})


@admin_required
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect("manage_users")


@admin_required
def reports(request):
    context = {
        "total_users": User.objects.count(),
        "total_vehicles": Vehicle.objects.count(),
        "total_documents": Documentation.objects.count(),
        "total_services": ServiceDetail.objects.count(),
        "total_transport": Transportation.objects.count(),
        "total_parking": ParkingDetails.objects.count(),
    }

    return render(request, "dashboard/reports.html", context)


@admin_required
def delete_vehicle(request, id):
    vehicle = Vehicle.objects.get(id=id)
    vehicle.delete()
    return redirect("vehicle_list")


@admin_required
def delete_document(request, id):
    doc = Documentation.objects.get(id=id)
    doc.delete()
    return redirect("document_list")

@login_required(login_url="login")
def update_service(request, id):
    service = get_object_or_404(ServiceDetail, id=id)

    if request.user.role != "admin":
        return redirect("service_list")

    if request.method == "POST":
        new_status = request.POST.get("status")

        # ✅ FIX: prevent NULL
        if new_status:
            service.status = new_status
            service.save()

        return redirect("service_list")

    return render(request, "service/update_service.html", {"service": service})



# from django.shortcuts import render , redirect , get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Vehicle , Documentation , ServiceDetail , Transportation , ParkingDetails 
# from .forms import VehicleForm , DocumentForm , ServiceForm , TransportForm , ParkingForm
# from django.contrib.auth import get_user_model
# from core.models import ServiceStaff , User
# ## ---------------- DASHBOARD ----------------
# @login_required(login_url="login")
# def dashboard(request):
#     role = request.user.role
#     context = {
#         "role": role,
#         "user": request.user
#     }

#     # -------- ADMIN --------
#     if role == "admin":
#         context.update({
#             "vehicles": Vehicle.objects.all(),  # Fetch ALL vehicles for Admin
#             "total_users": User.objects.count(),
#             "total_vehicles": Vehicle.objects.count(),
#             "total_services": ServiceDetail.objects.count(),
#             "total_transport": Transportation.objects.count(),
#         })

#     # -------- USER --------
#     elif role == "user":
#         context.update({
#             "vehicles": Vehicle.objects.filter(userId=request.user), # Fetch OWN vehicles
#             "services": ServiceDetail.objects.filter(vehicleId__userId=request.user),
#             "transports": Transportation.objects.filter(vehicleId__userId=request.user),
#         })

#     # -------- STAFF --------
#     elif role == "staff":
#         try:
#             staff = ServiceStaff.objects.get(user=request.user)
#             assigned_services = ServiceDetail.objects.filter(staffId=staff)
#         except ServiceStaff.DoesNotExist:
#             assigned_services = []

#         context.update({
#             "assigned_services": assigned_services
#         })
        
#     return render(request, "dashboard/dashboard.html", context)#@login_required(login_url="login")
# @login_required(login_url="login")
# def vehicle_list(request):
#     role = request.user.role # Added this line
#     if role == "admin":
#         vehicles = Vehicle.objects.all()
#     else:
#         vehicles = Vehicle.objects.filter(userId=request.user)

#     return render(request,'vehicle/vehicle_list.html',{
#         'vehicles': vehicles,
#         'role': role # Pass role to template for the footer
#     })
# @login_required(login_url="login")
# def add_vehicle(request):
#     form = VehicleForm()
#     if request.method == "POST":
#         # Change this line to include request.FILES
#         form = VehicleForm(request.POST, request.FILES) 
#         if form.is_valid():
#             vehicle = form.save(commit=False)
#             vehicle.userId = request.user
#             vehicle.save()
#             return redirect("vehicle_list")
#     return render(request,'vehicle/add_vehicle.html',{'form':form})

# def upload_document(request):

#     form = DocumentForm()

#     if request.method == "POST":

#         form = DocumentForm(request.POST, request.FILES)

#         if form.is_valid():
#             form.save()
#             return redirect('document_list')

#     return render(request,'documents/upload_document.html',{
#         'form':form
#     })


# @login_required(login_url="login")
# def document_list(request):

#     if request.user.role == "admin":
#         docs = Documentation.objects.all()
#     else:
#         docs = Documentation.objects.filter(vehicleId__userId=request.user)

#     return render(request, 'documents/document_list.html', {
#         'docs': docs
#     })

# @login_required(login_url="login")
# def add_service(request):

#     if request.method == "POST":
#         form = ServiceForm(request.POST, request.FILES)

#         # 🔥 IMPORTANT: filter vehicle for logged-in user
#         form.fields['vehicleId'].queryset = Vehicle.objects.filter(userId=request.user)

#         if form.is_valid():
#             service = form.save(commit=False)

#             # ❌ No staff assigned here (admin will assign)
#             service.save()

#             return redirect('service_list')
#         else:
#             print(form.errors)

#     else:
#         form = ServiceForm()

#         # 🔥 IMPORTANT LINE (THIS IS STEP 2 YOU DIDN’T UNDERSTAND)
#         form.fields['vehicleId'].queryset = Vehicle.objects.filter(userId=request.user)

#     return render(request, 'service/add_service.html', {'form': form})

# @login_required(login_url="login")
# def service_list(request):

#     if request.user.role == "admin":
#         services = ServiceDetail.objects.all()

#     elif request.user.role == "staff":
#         try:
#             staff = ServiceStaff.objects.get(user=request.user)
#             services = ServiceDetail.objects.filter(staffId=staff)
#         except ServiceStaff.DoesNotExist:
#             services = []

#     else:
#         services = ServiceDetail.objects.filter(vehicleId__userId=request.user)

#     return render(request, 'service/service_list.html', {
#         'services': services
#     })
# @login_required(login_url="login")
# def update_service(request, id):

#     service = get_object_or_404(ServiceDetail, id=id)

#     if request.user.role not in ["admin", "staff"]:
#         return redirect("service_list")

#     if request.method == "POST":
#         form = ServiceForm(request.POST, instance=service)

#         if form.is_valid():
#             form.save()
#             return redirect("service_list")

#     else:
#         form = ServiceForm(instance=service)

#     return render(request, "service/update_service.html", {"form": form})

# @login_required(login_url="login")
# def add_transport(request):

#     if request.method == "POST":
#         form = TransportForm(request.POST)

#         if form.is_valid():
#             transport = form.save(commit=False)
#             transport.userId = request.user
#             transport.save()
#             return redirect("transport_list")
#         else:
#             print("FORM ERRORS:", form.errors)

#     else:
#         form = TransportForm()

#         # 🔥 IMPORTANT
#         form.fields['vehicleId'].queryset = Vehicle.objects.filter(userId=request.user)

#     return render(request, "transport/add_transport.html", {"form": form})


# @login_required(login_url="login")
# def transport_list(request):

#     if request.user.role == "admin":
#         transports = Transportation.objects.all()
#     else:
#         transports = Transportation.objects.filter(vehicleId__userId=request.user)

#     return render(request, "transport/transport_list.html", {
#         "transports": transports
#     })

# @login_required(login_url="login")
# def update_transport(request, id):

#     transport = get_object_or_404(Transportation, id=id)

#     if request.user.role != "admin":
#         return redirect("transport_list")

#     if request.method == "POST":
#         form = TransportForm(request.POST, instance=transport)

#         if form.is_valid():
#             form.save()
#             return redirect("transport_list")

#     else:
#         form = TransportForm(instance=transport)

#     return render(request, "transport/update_transport.html", {"form": form})

# @login_required(login_url="login")
# def delete_transport(request, id):

#     transport = get_object_or_404(Transportation, id=id)

#     if request.user.role != "admin":
#         return redirect("transport_list")

#     transport.delete()
#     return redirect("transport_list")

# def parking_list(request):

#     parking = ParkingDetails.objects.all()

#     return render(request, "parking/parking_list.html", {"parking": parking})


# @login_required(login_url="login") # Add this to ensure request.user exists
# def parking_entry(request):
#     if request.method == "POST":
#         form = ParkingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("parking_list")
#     else:
#         form = ParkingForm()
#         # If your base.html requires 'role', add it here
#         role = getattr(request.user, 'role', 'user') 
        
#     return render(request, "parking/parking_entry.html", {
#         "form": form,
#         "role": role
#     })
# def admin_required(view_func):

#     def wrapper(request, *args, **kwargs):

#         if not request.user.is_authenticated:
#             return redirect("login")

#         if request.user.role != "admin":
#             return redirect("home")

#         return view_func(request, *args, **kwargs)

#     return wrapper

# @admin_required
# def manage_users(request):

#     users = User.objects.all()

#     return render(request,"dashboard/manage_users.html",{
#         "users":users
#     })

# @admin_required
# def delete_user(request, user_id):

#     user = User.objects.get(id=user_id)

#     user.delete()

#     return redirect("manage_users")

# @admin_required
# def reports(request):

#     total_users = User.objects.count()

#     total_vehicles = Vehicle.objects.count()

#     total_documents = Documentation.objects.count()

#     total_services = ServiceDetail.objects.count()

#     total_transport = Transportation.objects.count()

#     total_parking = ParkingDetails.objects.count()

#     context = {

#         "total_users":total_users,
#         "total_vehicles":total_vehicles,
#         "total_documents":total_documents,
#         "total_services":total_services,
#         "total_transport":total_transport,
#         "total_parking":total_parking,

#     }

#     return render(request,"dashboard/reports.html",context)

# @admin_required
# def delete_vehicle(request, id):

#     vehicle = Vehicle.objects.get(id=id)

#     vehicle.delete()

#     return redirect("vehicle_list")

# @admin_required
# def delete_document(request, id):

#     doc = Documentation.objects.get(id=id)

#     doc.delete()

#     return redirect("document_list")

# @login_required(login_url="login")
# def delete_service(request, id):

#     service = get_object_or_404(ServiceDetail, id=id)

#     if request.user.role != "admin":
#         return redirect("service_list")

#     service.delete()
#     return redirect("service_list")

# # @admin_required
# # def delete_transport(request, id):

# #     transport = Transportation.objects.get(id=id)

# #     transport.delete()

# #     return redirect("transport_list")
# @login_required(login_url="login")
# def delete_parking(request, id):
#     parking = get_object_or_404(ParkingDetails, id=id)

#     # PERMISSION CHECK:
#     # 1. User is Admin
#     # 2. OR the Vehicle in the parking record belongs to the logged-in User
#     if request.user.role == "admin" or parking.vehicleId.userId == request.user:
#         parking.delete()
#         return redirect("parking_list")
    
#     # If someone tries to delete a record they don't own
#     return redirect("parking_list")

