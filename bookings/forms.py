# bookings/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Patient, Doctor, Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'time': forms.widgets.TimeInput(attrs={'type': 'time'})
        }

class EditAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'reason']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['phone', 'address', 'sex']

class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialty']  # Removed user field since it will be assigned programmatically

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
