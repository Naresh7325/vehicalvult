from django.urls import path
from . import views

urlpatterns = [

    # path("user/",views.userDashboardView,name="user_dashboard"),
    # path("admin/",views.adminDashboardView,name="admin_dashboard"),
    # path("servicestaff/",views.servicestaffDashboardView,name="servicestaff_dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('vehicles/',views.vehicle_list,name="vehicle_list"),

path('add_vehicle/',views.add_vehicle,name="add_vehicle"),

path('documents/',views.document_list,name="document_list"),

path('upload_document/',views.upload_document,name="upload_document"),

path('services/', views.service_list, name="service_list"),
path('add_service/', views.add_service, name="add_service"),

path('service/update/<int:id>/', views.update_service, name="update_service"),
path('service/delete/<int:id>/', views.delete_service, name="delete_service"),
path('transport/',views.transport_list,name="transport_list"),

path("transport/", views.transport_list, name="transport_list"),
path("add_transport/", views.add_transport, name="add_transport"),
path("transport/update/<int:id>/", views.update_transport, name="update_transport"),
path("transport/delete/<int:id>/", views.delete_transport, name="delete_transport"),
path("parking/", views.parking_list, name="parking_list"),

path("parking/add/", views.parking_entry, name="parking_entry"),

path("dashboard/manage-users/", views.manage_users, name="manage_users"),

path("dashboard/delete-user/<int:user_id>/", views.delete_user, name="delete_user"),

path("dashboard/reports/", views.reports, name="reports"),

path("vehicle/delete/<int:id>/", views.delete_vehicle, name="delete_vehicle"),
path("document/delete/<int:id>/", views.delete_document, name="delete_document"),


path("parking/delete/<int:id>/", views.delete_parking, name="delete_parking"),


]