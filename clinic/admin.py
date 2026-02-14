from django.contrib import admin
from .models import Doctor, Service, Cabinet, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialization', 'experience_years', 'is_active']
    list_filter = ['specialization', 'is_active']
    search_fields = ['first_name', 'last_name', 'patronymic']
    list_editable = ['is_active']
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = "ФИО"
    full_name.admin_appointment_field = ['last_name', 'first_name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    list_editable = ['price', 'duration', 'is_active']


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ['number', 'floor']
    search_fields = ['number']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_last_name', 'patient_first_name', 'doctor', 'service', 'appointment_date', 'appointment_time', 'status']
    list_filter = ['status', 'appointment_date', 'doctor', 'service']
    search_fields = ['patient_last_name', 'patient_first_name', 'patient_phone']
    date_hierarchy = 'appointment_date'
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Информация о пациенте', {
            'fields': ['patient_last_name', 'patient_first_name', 'patient_patronymic', 
                      'patient_phone', 'patient_email', 'patient_birth_date']
        }),
        ('Детали приема', {
            'fields': ['doctor', 'service', 'cabinet', 'appointment_date', 'appointment_time', 'status']
        }),
        ('Дополнительно', {
            'fields': ['notes', 'created_at', 'updated_at']
        }),
    ]