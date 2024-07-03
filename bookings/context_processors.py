from .models import Patient, Doctor

def user_roles(request):
    if request.user.is_authenticated:
        is_patient = Patient.objects.filter(user=request.user).exists()
        is_doctor = Doctor.objects.filter(user=request.user).exists()
        return {
            'is_patient': is_patient,
            'is_doctor': is_doctor,
        }
    return {}