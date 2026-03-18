from django.db import models
# from django.contrib.auth.models import User 
from core.models import User , ServiceStaff


class Vehicle(models.Model):
    userId= models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)
    vehicle_color=models.CharField(max_length=100)
    vehicle_model=models.CharField(max_length=100)

    class Meta:
        db_table="Vehicle"

    def __str__(self):
        return self.vehicle_number

class Documentation(models.Model):
    vehicleId= models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=50)
    doc_file = models.FileField(upload_to='documents/')
    doc_number=models.CharField(max_length=100)
    expiry_date=models.DateField()

    class Meta:
        db_table="Documetation"

class ParkingDetails(models.Model):
    vehicleId= models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    parking_slot = models.CharField(max_length=50)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)
    daily_charge = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "parking_details"

    def __str__(self):
        return f"{self.vehicleId} - {self.parking_slot}"



class ServiceDetail(models.Model):
    vehicleId = models.ForeignKey("Vehicle", on_delete=models.CASCADE)
    staffId = models.ForeignKey(ServiceStaff, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    service_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")
    service_photo = models.ImageField(upload_to="service_photos/", null=True, blank=True)

class Transportation(models.Model):
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    date = models.DateField()   # REQUIRED
    vehicleId = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    class Meta:
        db_table="Transportation"

class Payment(models.Model):
    userId= models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    serviceId= models.OneToOneField(ServiceDetail, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    class Meta:
        db_table="Payment"




