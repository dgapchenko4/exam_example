from django.contrib import admin
from .models import Order, AppointmentItem, ServiceStatus, Filial

class OrderItemInline(admin.TabularInline):
    model = AppointmentItem
    extra = 1
    fields = ['product', 'quantity', 'price']

@admin.register(Order)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['appointment_number', 'customer', 'status', 'appointment_date', 'appointment_date']
    list_filter = ['status', 'appointment_date']
    search_fields = ['appointment_number', 'customer__username']
    inlines = [OrderItemInline]
    date_hierarchy = 'appointment_date'

@admin.register(ServiceStatus)
class ServiceStatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ['address']
    search_fields = ['address']
