from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Book, Genre, Author, Publisher
from .forms import BookForm


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
    """Список книг с учетом роли пользователя"""
    user_role = get_user_role(request.user) if request.user.is_authenticated else 'guest'

    # Базовый queryset для книг
    products = Book.objects.select_related('genre', 'author', 'publisher')
    
    # Получаем ВСЕ жанры для фильтра - ВАЖНО!
    categories = Genre.objects.all()  # Переменная должна называться 'categories'
    # ИЛИ если в шаблоне используется 'genres', то:
    # genres = Genre.objects.all()

    # Получаем выбранную категорию из GET-параметров
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(genre__id=category_filter)

    # Фильтры и поиск только для менеджеров и администраторов
    if user_role in ['manager', 'admin']:
        # Поиск
        search_query = request.GET.get('search', '')
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(genre__name__icontains=search_query) |
                Q(author__name__icontains=search_query) |
                Q(publisher__name__icontains(search_query))
            )

        # Фильтр по издательству
        publisher_filter = request.GET.get('publisher', '')
        if publisher_filter:
            products = products.filter(publisher__id=publisher_filter)

        # Сортировка
        sort_by = request.GET.get('sort', 'name')
        if sort_by == 'year_asc':
            products = products.order_by('year')
        elif sort_by == 'year_desc':
            products = products.order_by('-year')
        elif sort_by == 'price_asc':
            products = products.order_by('price')
        elif sort_by == 'price_desc':
            products = products.order_by('-price')
        else:
            products = products.order_by('name')

        publishers = Publisher.objects.all()
    else:
        publishers = None
        search_query = ''
        publisher_filter = ''
        sort_by = 'name'

    # Пагинация
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ДЛЯ ОТЛАДКИ - добавим принты
    print(f"DEBUG: categories count = {categories.count()}")
    print(f"DEBUG: products count = {products.count()}")
    print(f"DEBUG: page_obj count = {len(page_obj)}")

    context = {
        'page_obj': page_obj,
        'user_role': user_role,
        'categories': categories,  # Ключевая переменная!
        'category_filter': category_filter,
        'publishers': publishers,
        'search_query': search_query,
        'publisher_filter': publisher_filter,
        'sort_by': sort_by,
    }

    return render(request, 'products/product_list.html', context)


@login_required
def product_create(request):
    """Создание новой книги (только для администраторов)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('products:product_list')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Книга успешно создана.')
            return redirect('products:product_list')
    else:
        form = BookForm()

    # Используйте тот файл, который у вас реально существует
    return render(request, 'products/order_form.html', {  # или 'products/book_form.html'
        'form': form,
        'title': 'Добавить книгу',
        'user_role': get_user_role(request.user)
    })


@login_required
def product_update(request, pk):
    """Редактирование книги (только для администраторов)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('products:product_list')

    product = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Удаляем старое изображение, если оно заменено
            if 'image' in request.FILES and product.image:
                product.image.delete()
            form.save()
            messages.success(request, 'Книга успешно обновлена.')
            return redirect('products:product_list')
    else:
        form = BookForm(instance=product)

    # Используйте тот файл, который у вас реально существует
    return render(request, 'products/order_form.html', {  # или 'products/book_form.html'
        'form': form,
        'product': product,
        'title': 'Редактировать книгу',
        'user_role': get_user_role(request.user)
    })


@login_required
def product_delete(request, pk):
    """Удаление книги (только для администраторов)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('products:product_list')

    product = get_object_or_404(Book, pk=pk)

    # Проверяем, используется ли книга в заказах
    if hasattr(product, 'orderitem_set') and product.orderitem_set.exists():
        messages.error(request, 'Невозможно удалить книгу, которая присутствует в заказах.')
        return redirect('products:product_list')

    if request.method == 'POST':
        # Удаляем изображение
        if product.image:
            product.image.delete()
        product.delete()
        messages.success(request, 'Книга успешно удалена.')
        return redirect('products:product_list')

    return render(request, 'products/order_confirm_delete.html', {  # или 'products/book_confirm_delete.html'
        'product': product,
        'user_role': get_user_role(request.user)
    })

