# products/views.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, Brand  # Импортируем Brand вместо Manufacturer
from django.db.models import Q

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
            # Важно: в форме тоже нужно заменить author на brand
            # и manufacturer на brand


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
    """Список товаров - ИСПРАВЛЕНО"""
    products = Product.objects.all().select_related('brand')
    
    # Поиск - если добавите позже
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Фильтрация по бренду
    brand_id = request.GET.get('brand')
    if brand_id and brand_id != 'all':
        products = products.filter(brand_id=brand_id)
    
    # Сортировка
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-id')  # новые сначала
    
    # Пагинация
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Получаем все бренды для фильтра
    brands = Brand.objects.all().order_by('name')
    
    context = {
        'page_obj': page_obj,
        'brands': brands,
        'selected_brand': brand_id,
        'current_sort': sort,
        'search_query': query,
        'user_role': get_user_role(request.user)
    }
    return render(request, 'products/product_list.html', context)


@login_required
def product_create(request):
    """Создание нового товара"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Товар "{product.name}" успешно создан.')
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
    """Редактирование товара"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('product_list')

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Удаляем старое изображение, если загружено новое
            if 'image' in request.FILES and product.image:
                product.image.delete()
            product = form.save()
            messages.success(request, f'Товар "{product.name}" успешно обновлен.')
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
    """Удаление товара"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('product_list')

    product = get_object_or_404(Product, pk=pk)

    # Проверяем, используется ли товар в заказах
    try:
        from orders.models import OrderItem
        if OrderItem.objects.filter(product=product).exists():
            messages.error(request, 
                'Невозможно удалить товар, который присутствует в заказах.')
            return redirect('product_list')
    except ImportError:
        pass

    if request.method == 'POST':
        # Удаляем изображение
        if product.image:
            product.image.delete()
        product_name = product.name
        product.delete()
        messages.success(request, f'Товар "{product_name}" успешно удален.')
        return redirect('product_list')

    return render(request, 'products/product_confirm_delete.html', {
        'product': product,
        'user_role': get_user_role(request.user)
    })