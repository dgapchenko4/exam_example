import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')

import django
django.setup()

from products.models import *

# Очистка
Product.objects.all().delete()
Category.objects.all().delete()
Manufacturer.objects.all().delete()
Supplier.objects.all().delete()
Unit.objects.all().delete()

# Создание простых записей
m, _ = Manufacturer.objects.get_or_create(name="Test Manufacturer")
s, _ = Supplier.objects.get_or_create(name="Test Supplier")
u, _ = Unit.objects.get_or_create(name="шт", defaults={"abbreviation": "шт"})

# Создание категорий
cats = {}
for name in ["Кроссовки", "Туфли", "Ботинки", "Сандалии", "Сапоги"]:
    cat, _ = Category.objects.get_or_create(name=name)
    cats[name] = cat
    print(f"Категория: {name}")

# Создание товаров
products = [
    ("Nike Air Test", 8900, "Кроссовки", "Тестовые кроссовки"),
    ("Adidas Test", 9900, "Кроссовки", "Тестовые беговые кроссовки"),
    ("Кожаные туфли", 12900, "Туфли", "Тестовые кожаные туфли"),
    ("Зимние ботинки", 15900, "Ботинки", "Тестовые зимние ботинки"),
    ("Пляжные сандалии", 3900, "Сандалии", "Тестовые сандалии"),
]

for name, price, cat_name, desc in products:
    p = Product.objects.create(
        name=name,
        price=price,
        description=desc,
        category=cats[cat_name],
        manufacturer=m,
        supplier=s,
        unit=u,
        quantity=10
    )
    print(f"Товар: {name} - {price} руб.")

print(f"\nСоздано: {Product.objects.count()} товаров")