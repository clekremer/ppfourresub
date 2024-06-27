# bookings/views.py

from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Appointment
from django.contrib.auth.models import User
from .forms import UserForm, PatientForm
from .models import Patient

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'bookings/book_appointment.html', {'form': form})

def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'bookings/appointment_list.html', {'appointments': appointments})


def register_patient(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        patient_form = PatientForm(request.POST)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect('patient_list')
    else:
        user_form = UserForm()
        patient_form = PatientForm()
    return render(request, 'bookings/register_patient.html', {'user_form': user_form, 'patient_form': patient_form})


