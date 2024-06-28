
# bookings/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Patient
from .models import Appointment  # Adjusted import statement to import Appointment model

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment  # Using Appointment model from .models
        fields = ['patient', 'doctor', 'date', 'time', 'reason']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['phone', 'address']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
