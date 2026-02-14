from django import forms
from .models import Appointment, Doctor, Service

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'patient_last_name', 'patient_first_name', 'patient_patronymic',
            'patient_phone', 'patient_email', 'patient_birth_date',
            'doctor', 'service', 'appointment_date', 'appointment_time', 'notes'
        ]
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'patient_birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'patient_last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'patient_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'patient_last_name': 'Фамилия',
            'patient_first_name': 'Имя',
            'patient_patronymic': 'Отчество',
            'patient_phone': 'Телефон',
            'patient_email': 'Email',
            'patient_birth_date': 'Дата рождения',
            'doctor': 'Врач',
            'service': 'Услуга',
            'appointment_date': 'Дата приема',
            'appointment_time': 'Время приема',
            'notes': 'Примечания',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)
        self.fields['service'].queryset = Service.objects.filter(is_active=True)