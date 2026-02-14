from django import forms
from django.contrib.auth.models import User
from .models import Service, ServiceStatus, Filial, AppointmentItem


class ServiceForm(forms.ModelForm):
    """Форма для создания/редактирования заказа"""

    class Meta:
        model = Service
        fields = ['appointment_number', 'status', 'pickup_point', 'appointment_date', 'customer']
        widgets = {
            'appointment_number': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'pickup_point': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'customer': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем подсказки к полям
        self.fields['appointment_number'].help_text = 'Уникальный артикул заказа'
        self.fields['appointment_date'].help_text = 'Дата и время доставки (опционально)'