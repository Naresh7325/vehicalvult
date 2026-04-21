from django.db import models
# from django.contrib.auth.models import User 
from core.models import User , ServiceStaff


class Vehicle(models.Model):
    userId= models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_name=models.CharField(max_length=100 , null=False)
    vehicle_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)
    vehicle_photo = models.ImageField(upload_to='vehicle/', null=True, blank=True)
    vehicle_color=models.CharField(max_length=100)
    vehicle_model=models.CharField(max_length=100)

    class Meta:
        db_table="Vehicle"

    def __str__(self):
        return self.vehicle_name 

class Documentation(models.Model):
    vehicleId= models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=50)
    doc_file = models.FileField(upload_to='documents/')
    expiry_date=models.DateField()

    class Meta:
        db_table="Documetation"

class ParkingDetails(models.Model):
    vehicleId= models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)
    daily_charge = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "parking_details"

    def __str__(self):
        return f"{self.vehicleId} - {self.entry_time}"



class ServiceDetail(models.Model):
    vehicleId = models.ForeignKey("Vehicle", on_delete=models.CASCADE)

    service_type = models.CharField(max_length=100)
    service_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    status_choices = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    status = models.CharField(max_length=20, choices=status_choices, default='pending')

    service_photo = models.ImageField(upload_to="service_photos/", null=True, blank=True)

    def __str__(self):
        return f"{self.vehicleId} - {self.service_type}"

class Transportation(models.Model):
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    date = models.DateTimeField()   # REQUIRED
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




