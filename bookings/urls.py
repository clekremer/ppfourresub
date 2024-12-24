from django.urls import path
from . import views

from .views import (
    index, book_appointment, appointment_list, register_doctor_step1,
    doctor_dashboard, register_patient, patient_detail, patient_list,
    login_view, logout_view, patient_cancel_appointment
)


urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patient/', views.patient_detail, name='patient_detail'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path(
        'register_doctor_step1/',
        views.register_doctor_step1,
        name='register_doctor_step1'
    ),
    path(
        'register_doctor_step2/',
        views.register_doctor_step2,
        name='register_doctor_step2'
    ),
    path(
        'register_doctor_new_user/',
        views.register_doctor_new_user,
        name='register_doctor_new_user'
    ),
    path(
        'register_doctor_existing_user/',
        views.register_doctor_existing_user,
        name='register_doctor_existing_user'
    ),
    path(
        'doctor_dashboard/',
        views.doctor_dashboard,
        name='doctor_dashboard'
    ),
    path(
        'edit_appointment/<int:appointment_id>/',
        views.edit_appointment,
        name='edit_appointment'
    ),
    path(
        'cancel_appointment/<int:appointment_id>/',
        views.patient_cancel_appointment,
        name='patient_cancel_appointment'
    ),
    path(
        'bookings/appointment/<int:appointment_id>/details/',
        views.get_appointment_details,
        name='get_appointment_details'
    ),
]
