from django.db import models

class Doctor(models.Model):
    """Модель врача-стоматолога"""
    SPECIALIZATIONS = [
        ('THERAPIST', 'Терапевт'),
        ('SURGEON', 'Хирург'),
        ('ORTHODONTIST', 'Ортодонт'),
        ('ORTHOPEDIST', 'Ортопед'),
        ('PEDIATRIC', 'Детский стоматолог'),
        ('HYGIENIST', 'Гигиенист'),
        ('IMPLANTOLOGIST', 'Имплантолог'),
    ]

    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=50, blank=True, verbose_name="Отчество")
    specialization = models.CharField(max_length=20, choices=SPECIALIZATIONS, verbose_name="Специализация")
    experience_years = models.PositiveIntegerField(default=0, verbose_name="Стаж (лет)")
    description = models.TextField(blank=True, verbose_name="Описание")
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True, verbose_name="Фото")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"
    
    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip()
    
    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
        ordering = ['last_name', 'first_name']


class Service(models.Model):
    """Модель стоматологической услуги"""
    name = models.CharField(max_length=200, verbose_name="Наименование услуги")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(verbose_name="Длительность (минуты)")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['name']


class Cabinet(models.Model):
    """Модель кабинета"""
    number = models.CharField(max_length=10, verbose_name="Номер кабинета")
    floor = models.PositiveIntegerField(default=1, verbose_name="Этаж")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    def __str__(self):
        return f"Кабинет {self.number}"
    
    class Meta:
        verbose_name = "Кабинет"
        verbose_name_plural = "Кабинеты"


class Appointment(models.Model):
    """Модель записи на прием"""
    STATUS_CHOICES = [
        ('PENDING', 'Ожидает подтверждения'),
        ('CONFIRMED', 'Подтвержден'),
        ('COMPLETED', 'Завершен'),
        ('CANCELLED', 'Отменен'),
        ('NO_SHOW', 'Не явился'),
    ]
    
    patient_first_name = models.CharField(max_length=50, verbose_name="Имя пациента")
    patient_last_name = models.CharField(max_length=50, verbose_name="Фамилия пациента")
    patient_patronymic = models.CharField(max_length=50, blank=True, verbose_name="Отчество пациента")
    patient_phone = models.CharField(max_length=20, verbose_name="Телефон")
    patient_email = models.EmailField(blank=True, verbose_name="Email")
    patient_birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, verbose_name="Врач")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name="Услуга")
    cabinet = models.ForeignKey(Cabinet, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Кабинет")
    
    appointment_date = models.DateField(verbose_name="Дата приема")
    appointment_time = models.TimeField(verbose_name="Время приема")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Статус")
    
    notes = models.TextField(blank=True, verbose_name="Примечания")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return f"{self.patient_last_name} {self.patient_first_name} - {self.doctor} - {self.appointment_date}"
    
    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"
        ordering = ['-appointment_date', 'appointment_time']
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
    