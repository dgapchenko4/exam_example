import os
import re

# 1. Исправить products/models.py
print("Исправляем products/models.py...")
with open('products/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем Book на Product если нужно
if 'class Book' in content and 'class Product' not in content:
    content = content.replace('class Book', 'class Product')
    content = content.replace("verbose_name = \"Книга\"", "verbose_name = \"Товар\"")
    content = content.replace("verbose_name_plural = \"Книги\"", "verbose_name_plural = \"Товары\"")
    print("  - Book заменен на Product")
elif 'class Product' in content:
    print("  - Уже использует Product")

# Исправляем publisher на Publisher
if "'publisher'" in content:
    content = content.replace("'publisher'", "'Publisher'")
    print("  - Исправлен publisher на Publisher")

with open('products/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Исправить orders/models.py
print("\nИсправляем orders/models.py...")
with open('orders/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Исправляем ссылку на модель
if "'products.Book'" in content:
    content = content.replace("'products.Book'", "'products.Product'")
    print("  - products.Book заменен на products.Product")
elif "'products.Product'" in content:
    print("  - Уже использует products.Product")

with open('orders/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nГотово! Теперь выполните:")
print("python manage.py makemigrations")
print("python manage.py migrate")
