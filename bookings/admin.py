from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Patient, Doctor, Appointment
from django.utils.translation import gettext_lazy as _

admin.site.register(Patient)
admin.site.register(Doctor)
#admin.site.register(Appointment)


# Define an inline admin descriptor for Patient model
class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = 'patients'

# Define an inline admin descriptor for Doctor model
class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = 'doctors'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PatientInline, DoctorInline)
    
    list_display = ('username', 'email', 'is_staff', 'is_doctor', 'is_patient')
    
    def is_doctor(self, obj):
        return hasattr(obj, 'doctor')
    is_doctor.boolean = True
    is_doctor.short_description = 'Doctor'

    def is_patient(self, obj):
        return hasattr(obj, 'patient')
    is_patient.boolean = True
    is_patient.short_description = 'Patient'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'reason', 'status')
    list_filter = ('status', 'date', 'doctor')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            doctor = request.user.doctor
            return qs.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            return qs.none()

    def get_list_display(self, request):
        if request.user.is_superuser:
            return self.list_display + ('doctor',)
        return self.list_display

admin.site.register(Appointment, AppointmentAdmin)