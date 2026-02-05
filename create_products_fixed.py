import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')
django.setup()

from products.models import Category, Product
def clear_data():
    Product.objects.all().delete()
    Category.objects.all().delete()
    print("Данные очищены")

# Вызовите в начале main()
clear_data()

def create_categories():
    categories = [
        {"name": "Кроссовки", "slug": "krossovki"},
        {"name": "Ботинки", "slug": "botinki"},
        {"name": "Кеды", "slug": "kedi"},
        {"name": "Сандалии", "slug": "sandali"},
        {"name": "Туфли", "slug": "tufli"},
    ]
    
    for cat_data in categories:
        # Проверяем, существует ли категория с таким slug
        category, created = Category.objects.get_or_create(
            slug=cat_data["slug"],
            defaults={"name": cat_data["name"]}
        )
        if created:
            print(f"✓ Создана категория: {cat_data['name']}")
        else:
            print(f"↻ Категория уже существует: {cat_data['name']}")

def create_products():
    """Создаем товары"""
    # Удаляем существующие товары
    Product.objects.all().delete()
    
    # Кроссовки
    category = Category.objects.get(name='Кроссовки')
    products = [
        ('Nike Air Max 270', 8990, 'Стильные кроссовки с технологией Air Max'),
        ('Adidas Ultraboost', 10990, 'Беговые кроссовки с технологией Boost'),
        ('Reebok Nano X', 7990, 'Кроссовки для функционального тренинга'),
    ]
    
    for name, price, desc in products:
        Product.objects.create(
            name=name,
            description=desc,
            price=price,
            category=category,
        )
        print(f'✓ Создан товар: {name} - {price} руб.')
    
    # Туфли
    category = Category.objects.get(name='Туфли')
    products = [
        ('Кожаные туфли Oxford', 12990, 'Классические кожаные туфли черного цвета'),
        ('Туфли Derby', 9990, 'Полуформальные туфли коричневого цвета'),
        ('Лоферы', 8490, 'Комфортные туфли без шнуровки'),
    ]
    
    for name, price, desc in products:
        Product.objects.create(
            name=name,
            description=desc,
            price=price,
            category=category,
        )
        print(f'✓ Создан товар: {name} - {price} руб.')
    
    # Ботинки
    category = Category.objects.get(name='Ботинки')
    products = [
        ('Кожаные ботинки Timberland', 15990, 'Прочные кожаные ботинки для города'),
        ('Зимние ботинки', 11990, 'Теплые ботинки для холодной погоды'),
        ('Челси', 10990, 'Элегантные ботинки на резиновой подошве'),
    ]
    
    for name, price, desc in products:
        Product.objects.create(
            name=name,
            description=desc,
            price=price,
            category=category,
        )
        print(f'✓ Создан товар: {name} - {price} руб.')
    
    # Сандалии
    category = Category.objects.get(name='Сандалии')
    products = [
        ('Сандалии Birkenstock', 6990, 'Ортопедические сандалии для комфорта'),
        ('Пляжные сандалии', 2990, 'Легкие сандалии для отдыха'),
    ]
    
    for name, price, desc in products:
        Product.objects.create(
            name=name,
            description=desc,
            price=price,
            category=category,
        )
        print(f'✓ Создан товар: {name} - {price} руб.')
    
    # Сапоги
    category = Category.objects.get(name='Сапоги')
    products = [
        ('Угги', 8990, 'Теплые зимние сапоги из овчины'),
        ('Сапоги на каблуке', 13990, 'Элегантные сапоги для вечера'),
    ]
    
    for name, price, desc in products:
        Product.objects.create(
            name=name,
            description=desc,
            price=price,
            category=category,
        )
        print(f'✓ Создан товар: {name} - {price} руб.')

if __name__ == '__main__':
    print('=' * 50)
    print('Создание тестовых данных...')
    print('=' * 50)
    
    create_categories()
    print('\n' + '-' * 50)
    create_products()
    
    print('\n' + '=' * 50)
    print('Готово! Создано:')
    print(f'  Категорий: {Category.objects.count()}')
    print(f'  Товаров: {Product.objects.count()}')
    print('=' * 50)
