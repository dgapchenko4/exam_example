from django.db import models
from django.contrib.auth.models import User

class ServiceStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название статуса")
    
    class Meta:
        app_label = 'appointments'
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
    
    def __str__(self):
        return self.name

class Filial(models.Model):
    address = models.CharField(max_length=200, verbose_name="Адрес")
    
    class Meta:
        app_label = 'appointments'
        verbose_name = "Назначение"
        verbose_name_plural = "Назначения"
    
    def __str__(self):
        return self.address

class Service(models.Model):
    appointment_number = models.CharField(max_length=50, unique=True, verbose_name="Услуга")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пациент")
    status = models.ForeignKey(ServiceStatus, on_delete=models.PROTECT, verbose_name="Статус")
    class Meta:
        app_label = 'appointments'
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    
    def __str__(self):
        return self.appointment_number

class AppointmentItem(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.CASCADE, verbose_name="Назначение")
    class Meta:
        app_label = 'appointments'
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
    
    def __str__(self):
        return f"{self.appointment.name}"
