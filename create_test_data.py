import os
import django
import random
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')
django.setup()

from products.models import Category, Product

def create_categories():
    categories = [
        ('Кроссовки', 'Спортивная обувь'),
        ('Туфли', 'Классическая обувь'),
        ('Ботинки', 'Осенняя и зимняя обувь'),
        ('Сандалии', 'Летняя обувь'),
        ('Сапоги', 'Зимняя обувь'),
    ]
    
    for name, desc in categories:
        Category.objects.get_or_create(
            name=name,
            defaults={
                'description': desc,
                'slug': slugify(name)
            }
        )
    print('Категории созданы')

def create_products():
    # Кроссовки
    Product.objects.get_or_create(
        name='Nike Air Max 270',
        defaults={
            'description': 'Стильные кроссовки с технологией Air Max',
            'price': 8990,
            'category': Category.objects.get(name='Кроссовки'),
        }
    )
    
    Product.objects.get_or_create(
        name='Adidas Ultraboost',
        defaults={
            'description': 'Беговые кроссовки с технологией Boost',
            'price': 10990,
            'category': Category.objects.get(name='Кроссовки'),
        }
    )
    
    # Туфли
    Product.objects.get_or_create(
        name='Кожаные туфли Oxford',
        defaults={
            'description': 'Классические кожаные туфли черного цвета',
            'price': 12990,
            'category': Category.objects.get(name='Туфли'),
        }
    )
    
    # Ботинки
    Product.objects.get_or_create(
        name='Кожаные ботинки Timberland',
        defaults={
            'description': 'Прочные кожаные ботинки для города',
            'price': 15990,
            'category': Category.objects.get(name='Ботинки'),
        }
    )
    
    # Добавим еще товаров
    products = [
        ('Reebok Nano X', 7990, 'Кроссовки', 'Кроссовки для функционального тренинга'),
        ('Туфли Derby', 9990, 'Туфли', 'Полуформальные туфли коричневого цвета'),
        ('Зимние ботинки', 11990, 'Ботинки', 'Теплые ботинки для холодной погоды'),
        ('Сандалии Birkenstock', 6990, 'Сандалии', 'Ортопедические сандалии для комфорта'),
        ('Угги', 8990, 'Сапоги', 'Теплые зимние сапоги из овчины'),
    ]
    
    for name, price, category_name, desc in products:
        Product.objects.get_or_create(
            name=name,
            defaults={
                'description': desc,
                'price': price,
                'category': Category.objects.get(name=category_name),
            }
        )
    
    print('Товары созданы')

if __name__ == '__main__':
    create_categories()
    create_products()
    print(f'Готово! Создано {Category.objects.count()} категорий и {Product.objects.count()} товаров')
