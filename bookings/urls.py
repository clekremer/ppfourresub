# bookings/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    #path('add_patient/', views.add_patient, name='add_patient'),
    #path('add_doctor/', views.add_doctor, name='add_doctor'),
    #path('patients/', views.patient_list, name='patient_list'),
    #path('doctors/', views.doctor_list, name='doctor_list'),
    path('register_patient/', views.register_patient, name='register_patient'),
]
