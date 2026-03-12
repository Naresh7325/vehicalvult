from django import forms
from .models import Vehicle, Documentation, ServiceDetail, Transportation, ParkingDetails


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documentation
        fields = '__all__'


class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceDetail
        fields = '__all__'


class TransportForm(forms.ModelForm):
    class Meta:
        model = Transportation
        fields = '__all__'


class ParkingForm(forms.ModelForm):
    class Meta:
        model = ParkingDetails
        fields = '__all__'