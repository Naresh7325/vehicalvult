from django.urls import path
from . import views

urlpatterns = [

    path("user/",views.userDashboardView,name="user_dashboard"),
    path("admin/",views.adminDashboardView,name="admin_dashboard"),
    path("servicestaff/",views.servicestaffDashboardView,name="servicestaff_dashboard"),
    path('vehicles/',views.vehicle_list,name="vehicle_list"),

path('add_vehicle/',views.add_vehicle,name="add_vehicle"),

path('documents/',views.document_list,name="document_list"),

path('upload_document/',views.upload_document,name="upload_document"),

path('services/',views.service_list,name="service_list"),

path('add_service/',views.add_service,name="add_service"),

path('transport/',views.transport_list,name="transport_list"),

path('add_transport/',views.add_transport,name="add_transport"),

path("parking/", views.parking_list, name="parking_list"),

path("parking/add/", views.parking_entry, name="parking_entry"),

]