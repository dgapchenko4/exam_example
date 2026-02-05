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

def book_list(request):
    """Список книг с учетом роли пользователя"""
    user_role = get_user_role(request.user) if request.user.is_authenticated else 'guest'

    # Базовый queryset для книг
    books = Book.objects.select_related('genre', 'author', 'publisher')

    # Фильтр по жанру
    genre_filter = request.GET.get('genre', '')
    if genre_filter:
        books = books.filter(genre__id=genre_filter)

    # Фильтры и поиск только для менеджеров и администраторов
    if user_role in ['manager', 'admin']:
        # Поиск
        search_query = request.GET.get('search', '')
        if search_query:
            books = books.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(genre__name__icontains=search_query) |
                Q(author__name__icontains=search_query) |
                Q(publisher__name__icontains=search_query)
            )

        # Фильтр по издательству
        publisher_filter = request.GET.get('publisher', '')
        if publisher_filter:
            books = books.filter(publisher__id=publisher_filter)

        # Сортировка
        sort_by = request.GET.get('sort', 'name')
        if sort_by == 'year_asc':
            books = books.order_by('year')
        elif sort_by == 'year_desc':
            books = books.order_by('-year')
        elif sort_by == 'price_asc':
            books = books.order_by('price')
        elif sort_by == 'price_desc':
            books = books.order_by('-price')
        else:
            books = books.order_by('name')

        publishers = Publisher.objects.all()
    else:
        publishers = None
        search_query = ''
        publisher_filter = ''
        sort_by = 'name'

    # Получаем ВСЕ жанры для фильтра
    genres = Genre.objects.all()

    # Пагинация
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'user_role': user_role,
        'publishers': publishers,
        'search_query': search_query,
        'publisher_filter': publisher_filter,
        'sort_by': sort_by,
        'genres': genres,
        'selected_genre': genre_filter,
    }

    return render(request, 'products/product_list.html', context)

@login_required
def book_create(request):
    """Создание новой книги (только для администраторов)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('books:book_list')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Книга успешно создана.')
            return redirect('books:book_list')
    else:
        form = BookForm()

    return render(request, 'products/order_form.html', {
        'form': form,
        'title': 'Добавить книгу',
        'user_role': get_user_role(request.user)
    })


@login_required
def book_update(request, pk):
    """Редактирование книги (только для администраторов)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('products:product_list')

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            # Удаляем старое изображение, если оно заменено
            if 'image' in request.FILES and book.image:
                book.image.delete()
            form.save()
            messages.success(request, 'Книга успешно обновлена.')
            return redirect('products:product_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'products/order_form.html', {
        'form': form,
        'book': book,
        'title': 'Редактировать книгу',
        'user_role': get_user_role(request.user)
    })


@login_required
def book_delete(request, pk):
    """Удаление книги (только для администраторов)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('products:product_list')

    book = get_object_or_404(Book, pk=pk)

    # Проверяем, используется ли книга в заказах
    if hasattr(book, 'orderitem_set') and book.orderitem_set.exists():
        messages.error(request, 'Невозможно удалить книгу, которая присутствует в заказах.')
        return redirect('products:product_list')

    if request.method == 'POST':
        # Удаляем изображение
        if book.image:
            book.image.delete()
        book.delete()
        messages.success(request, 'Книга успешно удалена.')
        return redirect('products:product_list')

    return render(request, 'products/order_confirm_delete.html', {
        'book': book,
        'user_role': get_user_role(request.user)
    })

