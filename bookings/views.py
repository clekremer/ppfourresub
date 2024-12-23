from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import Group, User
from .forms import AppointmentForm, UserForm, PatientForm, DoctorRegistrationForm, EditAppointmentForm
from .models import Appointment, Patient, Doctor
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def redirect_to_admin_login_if_not_superuser(request):
    if not request.user.is_superuser:
        return redirect(f'{settings.ADMIN_URL}?next={request.path}')
    return None

def index(request):
    return render(request, 'index.html')

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            if appointment.date < date.today():
                messages.error(request, 'The appointment date cannot be in the past.')
                return redirect('book_appointment')
            appointment.patient = request.user.patient
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

def is_staff(user):
    return user.is_staff

def register_doctor_step1(request):
    redirect_response = redirect_to_admin_login_if_not_superuser(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        return redirect('register_doctor_step2')
    return render(request, 'bookings/register_doctor_step1.html')

def register_doctor_step2(request):
    redirect_response = redirect_to_admin_login_if_not_superuser(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        if 'new_user' in request.POST:
            return redirect('register_doctor_new_user')
        elif 'existing_user' in request.POST:
            return redirect('register_doctor_existing_user')
    return render(request, 'bookings/register_doctor_step2.html')

def register_doctor_new_user(request):
    redirect_response = redirect_to_admin_login_if_not_superuser(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        doctor_form = DoctorRegistrationForm(request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            doctor_group, _ = Group.objects.get_or_create(name='Doctor')
            user.groups.add(doctor_group)

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()

            messages.success(request, 'Doctor registered successfully.')
            return redirect('index')
    else:
        user_form = UserForm()
        doctor_form = DoctorRegistrationForm()

    return render(request, 'bookings/register_doctor_new_user.html', {'user_form': user_form, 'doctor_form': doctor_form})

def register_doctor_existing_user(request):
    redirect_response = redirect_to_admin_login_if_not_superuser(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        user_id = request.POST.get('user')
        doctor_form = DoctorRegistrationForm(request.POST)
        
        if doctor_form.is_valid():
            user = User.objects.get(id=user_id)

            doctor_group, _ = Group.objects.get_or_create(name='Doctor')
            user.groups.add(doctor_group)

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()

            messages.success(request, 'Existing user registered as doctor successfully.')
            return redirect('index')
    else:
        users = User.objects.all()
        doctor_form = DoctorRegistrationForm()

    return render(request, 'bookings/register_doctor_existing_user.html', {'users': users, 'doctor_form': doctor_form})

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

        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

        if status in ['approved', 'rejected']:
            if appointment.status == 'pending':
                appointment.status = status
                appointment.save()
                messages.success(request, f'Appointment {status} successfully.')
            else:
                messages.error(request, 'You can only approve or reject pending appointments.')

        elif status == 'canceled':
            if appointment.status in ['approved', 'rejected']:
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

            # Authenticate and log the user in after registration
            authenticated_user = authenticate(username=user.username, password=user_form.cleaned_data['password'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'Registration successful. You are now logged in.')
                return redirect('patient_detail')
            else:
                messages.error(request, 'There was an issue logging you in after registration. Please try logging in manually.')
                return redirect('login')
        else:
            messages.error(request, 'Failed to register. Please correct the errors.')
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
            if form.cleaned_data['date'] < date.today():
                messages.error(request, 'The appointment date cannot be in the past.')
                return redirect('edit_appointment', appointment_id=appointment_id)
            appointment = form.save(commit=False)
            appointment.status = 'pending'
            appointment.save()
            messages.success(request, 'Appointment updated successfully.')
            return redirect('patient_detail')
    else:
        form = EditAppointmentForm(instance=appointment)

    return render(request, 'bookings/edit_appointment.html', {
        'form': form,
        'appointment': appointment
    })


@login_required
def patient_detail(request):
    try:
        patient = Patient.objects.get(user=request.user)
        pending_appointments = Appointment.objects.filter(patient=patient, status='pending')
        other_appointments = Appointment.objects.filter(patient=patient).exclude(status='pending')
        
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
