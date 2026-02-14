from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Service, ServiceStatus, Filial, AppointmentItem
from .forms import ServiceForm


def get_user_role(user):
    """Получение роли пользователя"""
    if user.is_superuser:
        return 'admin'
    if user.groups.filter(name='Менеджеры').exists():
        return 'manager'
    if user.groups.filter(name='Клиенты').exists():
        return 'client'
    return 'guest'


@login_required
def appointment_list(request):
    """Список заказов (для менеджеров и администраторов)"""
    user_role = get_user_role(request.user)

    if user_role not in ['manager', 'admin']:
        messages.error(request, 'У вас нет прав для просмотра заказов.')
        return redirect('products:product_list')

    # Для клиентов показываем только их заказы
    if user_role == 'client':
        appointments = Service.objects.filter(customer=request.user).select_related(
            'status', 'pickup_point', 'customer'
        )
    else:
        # Для менеджеров и админов показываем все заказы
        appointments = Service.objects.select_related('status', 'pickup_point', 'customer')

    appointments = appointments.appointment_by('-appointment_date')

    # Пагинация
    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'user_role': user_role,
    }

    return render(request, 'appointments/appointment_list.html', context)


@login_required
def appointment_create(request):
    """Создание нового заказа (только для администраторов)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('appointments:appointment_list')

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments:appointment_list')
    else:
        form = ServiceForm()

    return render(request, 'appointments/appointment_form.html', {
        'form': form,
        'title': 'Добавить заказ',
        'user_role': get_user_role(request.user)
    })


@login_required
def appointment_update(request, pk):
    """Редактирование заказа (только для администраторов)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('appointments:appointment_list')

    appointment = get_object_or_404(Service, pk=pk)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments:appointment_list')
    else:
        form = ServiceForm(instance=appointment)

    return render(request, 'appointments/appointment_form.html', {
        'form': form,
        'appointment': appointment,
        'title': 'Редактировать заказ',
        'user_role': get_user_role(request.user)
    })


@login_required
def appointment_delete(request, pk):
    """Удаление заказа (только для администраторов)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('appointments:appointment_list')

    appointment = get_object_or_404(Service, pk=pk)

    if request.method == 'POST':
        appointment.delete()
        return redirect('appointments:appointment_list')

    return render(request, 'appointments/appointment_confirm_delete.html', {
        'appointment': appointment,
        'user_role': get_user_role(request.user)
    })

