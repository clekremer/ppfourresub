from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AppointmentForm, UserForm, PatientForm, DoctorRegistrationForm, EditAppointmentForm
from .models import Appointment, Patient, Doctor
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html')


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient  # Assign the logged-in patient to the appointment
            appointment.save()
            messages.success(request, 'Appointment booked successfully.')
            return redirect('patient_detail')
        else:
            messages.error(request, 'Failed to book appointment. Please correct the errors.')
    else:
        form = AppointmentForm()
    return render(request, 'bookings/book_appointment.html', {'form': form})


def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'bookings/appointment_list.html', {'appointments': appointments})


@staff_member_required
def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to home or another view
    else:
        form = DoctorRegistrationForm()
    return render(request, 'register_doctor.html', {'form': form})


@login_required
def doctor_dashboard(request):
    try:
        doctor = request.user.doctor
        pending_appointments = Appointment.objects.filter(doctor=doctor, status='pending')
        answered_appointments = Appointment.objects.filter(doctor=doctor).exclude(status='pending')
    except ObjectDoesNotExist:
        doctor = None
        pending_appointments = []
        answered_appointments = []

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        status = request.POST.get('status')

        # Get the appointment related to the doctor
        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

        # Handle approval and rejection for pending appointments
        if status in ['approved', 'rejected']:
            if appointment.status == 'pending':  # Approve or reject only pending appointments
                appointment.status = status
                appointment.save()
                messages.success(request, f'Appointment {status} successfully.')
            else:
                messages.error(request, 'You can only approve or reject pending appointments.')

        # Handle cancellation for answered appointments
        elif status == 'canceled':
            if appointment.status in ['approved', 'rejected']:  # Only allow canceling answered appointments
                appointment.status = status
                appointment.save()
                messages.success(request, 'Appointment canceled successfully.')
            else:
                messages.error(request, 'Cannot cancel a pending appointment.')

        else:
            messages.error(request, 'Invalid status.')

    return render(request, 'doctor_dashboard.html', {
        'doctor': doctor,
        'pending_appointments': pending_appointments,
        'answered_appointments': answered_appointments,
    })


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
            return redirect('patient_detail')
    else:
        user_form = UserForm()
        patient_form = PatientForm()
    return render(request, 'bookings/register_patient.html', {'user_form': user_form, 'patient_form': patient_form})


@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)

    if appointment.status == 'canceled':
        messages.error(request, 'Canceled appointments cannot be edited.')
        return redirect('patient_detail')

    if request.method == 'POST':
        form = EditAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = 'pending'  # Change the status to pending
            appointment.save()
            messages.success(request, 'Appointment updated successfully.')
            return redirect('patient_detail')
        else:
            messages.error(request, 'Failed to update appointment. Please correct the errors.')

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def patient_detail(request):
    try:
        patient = Patient.objects.get(user=request.user)
        pending_appointments = Appointment.objects.filter(patient=patient, status='pending')
        other_appointments = Appointment.objects.filter(patient=patient).exclude(status='pending')
        
        # Organize other appointments by status
        appointments_by_status = {}
        for appointment in other_appointments:
            if appointment.status not in appointments_by_status:
                appointments_by_status[appointment.status] = []
            appointments_by_status[appointment.status].append(appointment)
        
        return render(request, 'bookings/patient_detail.html', {
            'patient': patient,
            'pending_appointments': pending_appointments,
            'appointments_by_status': appointments_by_status,
        })
    except ObjectDoesNotExist:
        messages.error(request, "Patient details not found.")
        return redirect('index')


@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'bookings/patient_list.html', {'patients': patients})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if hasattr(user, 'patient'):
                    return redirect('patient_detail')
                elif hasattr(user, 'doctor'):
                    return redirect('doctor_dashboard')
                else:
                    return render(request, 'role_not_assigned.html')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'bookings/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


@login_required
def patient_cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)
    
    if appointment.status in ['pending', 'approved']:
        appointment.status = 'canceled'
        appointment.save()
        messages.success(request, 'Appointment canceled successfully.')
    else:
        messages.error(request, 'Only pending or approved appointments can be canceled.')
    
    return redirect('patient_detail')
