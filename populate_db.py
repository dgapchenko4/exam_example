import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')
django.setup()

from products.models import Category, Manufacturer, Supplier, Unit, Product
from orders.models import OrderStatus, PickupPoint, Order
from django.contrib.auth.models import User, Group
from django.utils import timezone

def create_categories():
    """Создание категорий (жанров) книг"""
    categories = [
        'Фантастика',
        'Фэнтези',
        'Детектив',
        'Роман',
        'Приключения',
        'Научная литература',
        'Бизнес-литература',
        'Психология',
        'История',
        'Биография'
    ]
    for name in categories:
        Category.objects.get_or_create(name=name)
    print(f"Создано категорий: {Category.objects.count()}")

def create_manufacturers():
    """Создание производителей (издательств)"""
    publishers = [
        'Эксмо',
        'АСТ',
        'Питер',
        'Манн, Иванов и Фербер',
        'Альпина Паблишер',
        'Росмэн',
        'Дрофа',
        'Просвещение'
    ]
    for name in publishers:
        Manufacturer.objects.get_or_create(name=name)
    print(f"Создано издательств: {Manufacturer.objects.count()}")

def create_units():
    """Создание единиц измерения"""
    units = [
        ('шт', 'штука'),
        ('экз', 'экземпляр'),
    ]
    for abbreviation, name in units:
        Unit.objects.get_or_create(
            name=name,
            defaults={'abbreviation': abbreviation}
        )
    print(f"Создано единиц измерения: {Unit.objects.count()}")

def create_products():
    """Создание книг (товаров)"""
    # Получаем объекты
    fantasy = Category.objects.get(name='Фантастика')
    detective = Category.objects.get(name='Детектив')
    roman = Category.objects.get(name='Роман')
    
    exmo = Manufacturer.objects.get(name='Эксмо')
    ast = Manufacturer.objects.get(name='АСТ')
    piter = Manufacturer.objects.get(name='Питер')
    
    supplier, _ = Supplier.objects.get_or_create(name='Книжный опт')
    unit = Unit.objects.get(name='штука')
    
    # Список книг
    books = [
        {
            'name': '1984',
            'category': fantasy,
            'manufacturer': ast,
            'supplier': supplier,
            'price': 450.00,
            'unit': unit,
            'quantity': 25,
            'discount': 10.00,
            'description': 'Роман-антиутопия Джорджа Оруэлла'
        },
        {
            'name': 'Убийство в Восточном экспрессе',
            'category': detective,
            'manufacturer': exmo,
            'supplier': supplier,
            'price': 380.00,
            'unit': unit,
            'quantity': 15,
            'discount': 5.00,
            'description': 'Детектив Агаты Кристи'
        },
        {
            'name': 'Война и мир',
            'category': roman,
            'manufacturer': exmo,
            'supplier': supplier,
            'price': 890.00,
            'unit': unit,
            'quantity': 30,
            'discount': 15.00,
            'description': 'Роман-эпопея Льва Толстого'
        },
        {
            'name': 'Мастер и Маргарита',
            'category': roman,
            'manufacturer': ast,
            'supplier': supplier,
            'price': 520.00,
            'unit': unit,
            'quantity': 20,
            'discount': 0.00,
            'description': 'Роман Михаила Булгакова'
        },
        {
            'name': 'Преступление и наказание',
            'category': roman,
            'manufacturer': piter,
            'supplier': supplier,
            'price': 410.00,
            'unit': unit,
            'quantity': 18,
            'discount': 8.00,
            'description': 'Роман Фёдора Достоевского'
        },
    ]
    
    for book_data in books:
        Product.objects.get_or_create(
            name=book_data['name'],
            defaults=book_data
        )
    print(f"Создано книг: {Product.objects.count()}")

def main():
    print("Начало заполнения базы данных...")
    print("-" * 40)
    
    create_categories()
    create_manufacturers()
    create_units()
    create_products()
    
    print("-" * 40)
    print("База данных успешно заполнена!")

if __name__ == '__main__':
    main()