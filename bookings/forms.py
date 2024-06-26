
# bookings/forms.py

from django import forms
from .models import Appointment  # Adjusted import statement to import Appointment model

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment  # Using Appointment model from .models
        fields = ['patient', 'doctor', 'date', 'time', 'reason']
