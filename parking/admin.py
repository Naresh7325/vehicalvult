from django.contrib import admin
from .models import Vehicle, Documentation, ServiceDetail, Transportation, ParkingDetails

admin.site.register(Vehicle)
admin.site.register(Documentation)
admin.site.register(ServiceDetail)
admin.site.register(Transportation)
admin.site.register(ParkingDetails)