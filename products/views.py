# products/views.py - временная версия без django_filters
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, Brand

# Убрали импорт django_filters

try:
    from .forms import ProductForm
    FORM_EXISTS = True
except ImportError:
    FORM_EXISTS = False
    from django import forms
    class ProductForm(forms.ModelForm):
        class Meta:
            model = Product
            fields = '__all__'


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


def product_list(request):
    """Список товаров"""
    # Используем только существующие поля
    products = Product.objects.all()
    
    # Убираем фильтрацию по manufacturer
    # Убираем select_related
    
    # Пагинация с сортировкой
    products = products.order_by('-id')  # добавляем сортировку
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'user_role': get_user_role(request.user)
    }
    return render(request, 'products/product_list.html', context)


@login_required
def product_create(request):
    """Создание нового товара (только для администраторов)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно создан.')
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Добавить товар',
        'user_role': get_user_role(request.user)
    })


@login_required
def product_update(request, pk):
    """Редактирование товара (только для администраторов)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('product_list')

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Удаляем старое изображение, если оно заменено
            if 'image' in request.FILES and product.image:
                product.image.delete()
            form.save()
            messages.success(request, 'Товар успешно обновлен.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'product': product,
        'title': 'Редактировать товар',
        'user_role': get_user_role(request.user)
    })


@login_required
def product_delete(request, pk):
    """Удаление товара (только для администраторов)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('product_list')

    product = get_object_or_404(Product, pk=pk)

    # Проверяем, используется ли товар в заказах
    try:
        from orders.models import OrderItem
        if OrderItem.objects.filter(product=product).exists():
            messages.error(request, 'Невозможно удалить товар, который присутствует в заказах.')
            return redirect('product_list')
    except ImportError:
        pass

    if request.method == 'POST':
        # Удаляем изображение
        if product.image:
            product.image.delete()
        product.delete()
        messages.success(request, 'Товар успешно удален.')
        return redirect('product_list')

    return render(request, 'products/product_confirm_delete.html', {
        'product': product,
        'user_role': get_user_role(request.user)
    })