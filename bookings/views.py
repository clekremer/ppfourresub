# bookings/views.py

from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Appointment

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
