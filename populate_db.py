#!/usr/bin/env python
"""
Скрипт для заполнения базы данных тестовыми данными
Запускать через: python manage.py shell < populate_db.py
"""

from products.models import Category, Manufacturer, Supplier, Unit, Product
from orders.models import OrderStatus, PickupPoint, Order


def create_groups():
    """Создание групп пользователей"""
    groups = ['Клиенты', 'Менеджеры']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
    print("Группы пользователей созданы")


def create_test_users():
    """Создание тестовых пользователей"""
    # Администратор
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Админ',
            'last_name': 'Админович',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print("Администратор создан: admin/admin123")

    # Менеджер
    manager, created = User.objects.get_or_create(
        username='manager',
        defaults={
            'email': 'manager@example.com',
            'first_name': 'Менеджер',
            'last_name': 'Менеджерович'
        }
    )
    if created:
        manager.set_password('manager123')
        manager.save()
        manager.groups.add(Group.objects.get(name='Менеджеры'))
        print("Менеджер создан: manager/manager123")

    # Клиент
    client, created = User.objects.get_or_create(
        username='client',
        defaults={
            'email': 'client@example.com',
            'first_name': 'Клиент',
            'last_name': 'Клиентович'
        }
    )
    if created:
        client.set_password('client123')
        client.save()
        client.groups.add(Group.objects.get(name='Клиенты'))
        print("Клиент создан: client/client123")


def create_categories():
    """Создание категорий товаров"""
    categories = [
        'Кроссовки', 'Ботинки', 'Туфли', 'Сандалии', 'Сапоги',
        'Кеды', 'Балетки', 'Лоферы', 'Мокасины', 'Слипоны'
    ]
    for category_name in categories:
        Category.objects.get_or_create(name=category_name)
    print("Категории созданы")


def create_manufacturers():
    """Создание производителей"""
    manufacturers = [
        'Nike', 'Adidas', 'Puma', 'Reebok', 'New Balance',
        'Converse', 'Vans', 'Under Armour', 'Asics', 'Fila'
    ]
    for manufacturer_name in manufacturers:
        Manufacturer.objects.get_or_create(name=manufacturer_name)
    print("Производители созданы")


def create_suppliers():
    """Создание поставщиков"""
    suppliers = [
        'Спорттовары ООО', 'Обувь Оптом', 'Шуз ООО',
        'Футwear Plus', 'StepByStep'
    ]
    for supplier_name in suppliers:
        Supplier.objects.get_or_create(name=supplier_name)
    print("Поставщики созданы")


def create_units():
    """Создание единиц измерения"""
    units = [
        ('шт', 'штук'),
        ('пар', 'пар'),
        ('уп', 'упаковок'),
    ]
    for abbreviation, name in units:
        Unit.objects.get_or_create(
            name=name,
            defaults={'abbreviation': abbreviation}
        )
    print("Единицы измерения созданы")


def create_products():
    """Создание товаров"""
    categories = list(Category.objects.all())
    manufacturers = list(Manufacturer.objects.all())
    suppliers = list(Supplier.objects.all())
    units = list(Unit.objects.all())

    products_data = [
        {
            'name': 'Nike Air Max 270',
            'category': categories[0],
            'manufacturer': manufacturers[0],
            'supplier': suppliers[0],
            'price': 12990.00,
            'unit': units[0],
            'quantity': 25,
            'discount': 10.00,
            'description': 'Удобные кроссовки для бега с амортизацией'
        },
        {
            'name': 'Adidas Ultraboost 22',
            'category': categories[0],
            'manufacturer': manufacturers[1],
            'supplier': suppliers[1],
            'price': 15990.00,
            'unit': units[0],
            'quantity': 18,
            'discount': 15.00,
            'description': 'Профессиональные беговые кроссовки'
        },
        {
            'name': 'Puma RS-X³',
            'category': categories[0],
            'manufacturer': manufacturers[2],
            'supplier': suppliers[2],
            'price': 8990.00,
            'unit': units[0],
            'quantity': 0,
            'discount': 5.00,
            'description': 'Стильные кроссовки в ретро стиле'
        },
        {
            'name': 'Timberland 6-Inch Boot',
            'category': categories[4],
            'manufacturer': manufacturers[7],
            'supplier': suppliers[3],
            'price': 18990.00,
            'unit': units[0],
            'quantity': 12,
            'discount': 20.00,
            'description': 'Классические зимние сапоги'
        },
        {
            'name': 'Converse Chuck Taylor All Star',
            'category': categories[5],
            'manufacturer': manufacturers[5],
            'supplier': suppliers[4],
            'price': 5990.00,
            'unit': units[0],
            'quantity': 35,
            'discount': 0.00,
            'description': 'Классические кеды на все случаи жизни'
        },
        {
            'name': 'Vans Old Skool',
            'category': categories[5],
            'manufacturer': manufacturers[6],
            'supplier': suppliers[0],
            'price': 6990.00,
            'unit': units[0],
            'quantity': 8,
            'discount': 25.00,
            'description': 'Скейтбординговые кеды с боковой полосой'
        },
    ]

    for product_data in products_data:
        Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
    print("Товары созданы")


def create_order_statuses():
    """Создание статусов заказов"""
    statuses = [
        'Новый', 'В обработке', 'Готов к выдаче', 'Выдан', 'Отменен'
    ]
    for status_name in statuses:
        OrderStatus.objects.get_or_create(name=status_name)
    print("Статусы заказов созданы")


def create_pickup_points():
    """Создание пунктов выдачи"""
    points = [
        'ул. Ленина, 1',
        'пр. Победы, 25',
        'ул. Советская, 15',
        'ул. Гагарина, 7',
        'ТЦ "Центральный", 3 этаж'
    ]
    for address in points:
        PickupPoint.objects.get_or_create(address=address)
    print("Пункты выдачи созданы")


def create_orders():
    """Создание тестовых заказов"""
    from django.utils import timezone
    import random

    statuses = list(OrderStatus.objects.all())
    pickup_points = list(PickupPoint.objects.all())
    clients = list(User.objects.filter(groups__name='Клиенты'))

    if not clients:
        print("Нет клиентов для создания заказов")
        return

    orders_data = [
        {
            'order_number': 'ORD-001',
            'status': statuses[0],
            'pickup_point': pickup_points[0],
            'customer': clients[0],
            'delivery_date': timezone.now() + timezone.timedelta(days=3)
        },
        {
            'order_number': 'ORD-002',
            'status': statuses[1],
            'pickup_point': pickup_points[1],
            'customer': clients[0],
            'delivery_date': timezone.now() + timezone.timedelta(days=1)
        },
        {
            'order_number': 'ORD-003',
            'status': statuses[3],
            'pickup_point': pickup_points[2],
            'customer': clients[0] if clients else None,
            'delivery_date': timezone.now() - timezone.timedelta(days=1)
        },
    ]

    for order_data in orders_data:
        Order.objects.get_or_create(
            order_number=order_data['order_number'],
            defaults=order_data
        )
    print("Заказы созданы")


def main():
    """Основная функция"""
    print("Начало заполнения базы данных...")

    create_groups()
    create_test_users()
    create_categories()
    create_manufacturers()
    create_suppliers()
    create_units()
    create_products()
    create_order_statuses()
    create_pickup_points()
    create_orders()

    print("База данных успешно заполнена!")


if __name__ == '__main__':
    main()