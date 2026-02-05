import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')
django.setup()

from products.models import Category, Product, Manufacturer, Supplier, Unit

def create_manufacturers():
    """Создание производителей"""
    manufacturers = [
        'Nike',
        'Adidas', 
        'Reebok',
        'Puma',
        'New Balance'
    ]
    
    for name in manufacturers:
        Manufacturer.objects.get_or_create(name=name)
        print(f"✓ Производитель: {name}")
    
    return Manufacturer.objects.first()

def create_suppliers():
    """Создание поставщиков"""
    suppliers = [
        'Основной поставщик',
        'Дополнительный поставщик',
        'Оптовый поставщик'
    ]
    
    for name in suppliers:
        Supplier.objects.get_or_create(name=name)
        print(f"✓ Поставщик: {name}")
    
    return Supplier.objects.first()

def create_units():
    """Создание единиц измерения"""
    units = [
        ('штука', 'шт'),
        ('пара', 'пар'),
        ('упаковка', 'уп'),
    ]
    
    for name, abbreviation in units:
        Unit.objects.get_or_create(
            name=name,
            defaults={'abbreviation': abbreviation}
        )
        print(f"✓ Единица измерения: {name}")
    
    return Unit.objects.first()

def create_categories():
    """Создание категорий с уникальными slug"""
    categories_data = [
        ("Кроссовки", "Спортивная обувь"),
        ("Туфли", "Классическая обувь"),
        ("Ботинки", "Осенняя и зимняя обувь"),
        ("Сандалии", "Летняя обувь"),
        ("Сапоги", "Зимняя обувь"),
    ]
    
    created_cats = {}
    for name, desc in categories_data:
        # Создаем уникальный slug
        slug = slugify(name)
        
        # Проверяем и делаем slug уникальным если нужно
        counter = 1
        original_slug = slug
        while Category.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        cat, created = Category.objects.get_or_create(
            name=name,
            defaults={
                'description': desc,
                'slug': slug
            }
        )
        created_cats[name] = cat
        print(f"✓ Категория: {name}")
    
    return created_cats

def create_products(categories, manufacturer, supplier, unit):
    """Создание товаров"""
    products_data = [
        ("Nike Air Max 270", 8990, "Кроссовки", "Стильные кроссовки с технологией Air Max"),
        ("Adidas Ultraboost", 10990, "Кроссовки", "Беговые кроссовки с технологией Boost"),
        ("Reebok Nano X", 7990, "Кроссовки", "Кроссовки для функционального тренинга"),
        ("Кожаные туфли Oxford", 12990, "Туфли", "Классические кожаные туфли черного цвета"),
        ("Туфли Derby", 9990, "Туфли", "Полуформальные туфли коричневого цвета"),
        ("Лоферы", 8490, "Туфли", "Комфортные туфли без шнуровки"),
        ("Кожаные ботинки Timberland", 15990, "Ботинки", "Прочные кожаные ботинки для города"),
        ("Зимние ботинки", 11990, "Ботинки", "Теплые ботинки для холодной погоды"),
        ("Челси", 10990, "Ботинки", "Элегантные ботинки на резиновой подошве"),
        ("Сандалии Birkenstock", 6990, "Сандалии", "Ортопедические сандалии для комфорта"),
        ("Пляжные сандалии", 2990, "Сандалии", "Легкие сандалии для отдыха"),
        ("Угги", 8990, "Сапоги", "Теплые зимние сапоги из овчины"),
        ("Сапоги на каблуке", 13990, "Сапоги", "Элегантные сапоги для вечера"),
    ]
    
    for name, price, category_name, desc in products_data:
        # Используем get_or_create с полным набором полей
        product, created = Product.objects.get_or_create(
            name=name,
            defaults={
                'description': desc,
                'price': price,
                'category': categories[category_name],
                'manufacturer': manufacturer,
                'supplier': supplier,
                'unit': unit,
                'quantity': 10,
            }
        )
        if created:
            print(f"✓ Товар: {name} - {price} руб.")
        else:
            print(f"↻ Товар уже существует: {name}")

def main():
    print("=" * 50)
    print("Создание полного набора тестовых данных...")
    print("=" * 50)
    
    # Создаем связанные модели
    manufacturer = create_manufacturers()
    supplier = create_suppliers()
    unit = create_units()
    
    # Создаем категории
    categories = create_categories()
    
    # Создаем товары
    create_products(categories, manufacturer, supplier, unit)
    
    # Выводим итоги
    print("\n" + "=" * 50)
    print("✅ Готово! Создано:")
    print(f"   Производителей: {Manufacturer.objects.count()}")
    print(f"   Поставщиков: {Supplier.objects.count()}")
    print(f"   Единиц измерения: {Unit.objects.count()}")
    print(f"   Категорий: {Category.objects.count()}")
    print(f"   Товаров: {Product.objects.count()}")
    print("=" * 50)

if __name__ == '__main__':
    main()
