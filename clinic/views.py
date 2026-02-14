from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Doctor, Service, Appointment
from .forms import AppointmentForm

def get_user_role(user):
    """Получение роли пользователя"""
    if not user or not user.is_authenticated:
        return 'guest'
    if user.is_superuser:
        return 'admin'
    if user.groups.filter(name='Менеджеры').exists():
        return 'manager'
    if user.groups.filter(name='Клиенты').exists():
        return 'client'
    return 'user'


def doctor_list(request):
    """Список врачей"""
    doctors = Doctor.objects.filter(is_active=True)
    
    # Фильтрация по специализации
    specialization = request.GET.get('specialization')
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    
    paginator = Paginator(doctors, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'specializations': Doctor.SPECIALIZATIONS,
        'selected_specialization': specialization,
        'user_role': get_user_role(request.user)
    }
    return render(request, 'clinic/doctor_list.html', context)


def doctor_detail(request, pk):
    """Детальная страница врача"""
    doctor = get_object_or_404(Doctor, pk=pk)
    context = {
        'doctor': doctor,
        'user_role': get_user_role(request.user)
    }
    return render(request, 'clinic/doctor_detail.html', context)


def service_list(request):
    """Список услуг"""
    services = Service.objects.filter(is_active=True)
    
    paginator = Paginator(services, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'user_role': get_user_role(request.user)
    }
    return render(request, 'clinic/service_list.html', context)


def appointment_create(request):
    """Создание записи на прием"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, 'Запись на прием успешно создана! Ожидайте подтверждения.')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm()
    
    context = {
        'form': form,
        'user_role': get_user_role(request.user)
    }
    return render(request, 'clinic/appointment_form.html', context)


def appointment_detail(request, pk):
    """Детальная страница записи"""
    appointment = get_object_or_404(Appointment, pk=pk)
    context = {
        'appointment': appointment,
        'user_role': get_user_role(request.user)
    }
    return render(request, 'clinic/appointment_detail.html', context)


@login_required
def appointment_list(request):
    """Список записей (для администратора)"""
    if not request.user.is_staff:
        messages.error(request, 'Доступ запрещен')
        return redirect('doctor_list')
    
    appointments = Appointment.objects.all()
    
    # Фильтрация
    status = request.GET.get('status')
    if status:
        appointments = appointments.filter(status=status)
    
    date = request.GET.get('date')
    if date:
        appointments = appointments.filter(appointment_date=date)
    
    paginator = Paginator(appointments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': Appointment.STATUS_CHOICES,
        'user_role': get_user_role(request.user)
    }
    return render(request, 'clinic/appointment_list.html', context)