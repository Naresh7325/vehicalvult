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
        fields = ['vehicleId', 'service_type', 'service_date', 'cost', 'service_photo']

class TransportForm(forms.ModelForm):
    class Meta:
        model = Transportation
        fields = '__all__'

        widgets = {
            'date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'   # ✅ IMPORTANT FIX
            )
        }

    # ✅ REQUIRED to convert input properly
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date'].input_formats = ('%Y-%m-%dT%H:%M',)


class ParkingForm(forms.ModelForm):
    class Meta:
        model = ParkingDetails
        fields = '__all__'

        widgets = {
            'entry_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'exit_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['entry_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['exit_time'].input_formats = ('%Y-%m-%dT%H:%M',)