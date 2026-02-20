import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import (Category, Manufacturer, Supplier, Product,
                         Profile, PickupPoint, Order, OrderItem)
from datetime import datetime
import os
import shutil
from decimal import Decimal

class Command(BaseCommand):
    help = 'Импорт данных из Excel файлов'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем импорт...')

        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Manufacturer.objects.all().delete()
        Supplier.objects.all().delete()
        PickupPoint.objects.all().delete()

        df_tovar = pd.read_excel('import/Tovar.xlsx')
        categories = set(df_tovar['Категория товара'].dropna())
        for cat in categories:
            Category.objects.get_or_create(name=cat)

        manufacturers = set(df_tovar['Производитель'].dropna())
        for man in manufacturers:
            Manufacturer.objects.get_or_create(name=man)

        suppliers = set(df_tovar['Поставщик'].dropna())
        for sup in suppliers:
            Supplier.objects.get_or_create(name=sup)

        os.makedirs('media/products', exist_ok=True)
        for idx, row in df_tovar.iterrows():
            category = Category.objects.get(name=row['Категория товара'])
            manufacturer = Manufacturer.objects.get(name=row['Производитель'])
            supplier = Supplier.objects.get(name=row['Поставщик'])

            photo_filename = row.get('Фото', '')
            photo_field = None
            if photo_filename and pd.notna(photo_filename):
                src = f'import/{photo_filename}'
                if os.path.exists(src):
                    dst = f'media/products/{photo_filename}'
                    shutil.copy2(src, dst)
                    photo_field = f'products/{photo_filename}'

            Product.objects.get_or_create(
                article=row['Артикул'],
                defaults={
                    'name': row['Наименование товара'],
                    'unit': row['Единица измерения'],
                    'price': Decimal(str(row['Цена'])),
                    'supplier': supplier,
                    'manufacturer': manufacturer,
                    'category': category,
                    'discount': int(row['Действующая скидка']) if pd.notna(row['Действующая скидка']) else 0,
                    'quantity_in_stock': int(row['Кол-во на складе']) if pd.notna(row['Кол-во на складе']) else 0,
                    'description': row['Описание товара'] if pd.notna(row['Описание товара']) else '',
                    'photo': photo_field,
                }
            )

        df_users = pd.read_excel('import/user_import.xlsx')
        for idx, row in df_users.iterrows():
            email = row['Логин']
            password = row['Пароль']
            full_name = row['ФИО']
            role_map = {
                'Администратор': 'admin',
                'Менеджер': 'manager',
                'Авторизированный клиент': 'client',
            }
            role = role_map.get(row['Роль сотрудника'], 'client')
            user, created = User.objects.get_or_create(username=email, defaults={'email': email})
            if created:
                user.set_password(password)
                user.save()
            Profile.objects.update_or_create(user=user, defaults={'full_name': full_name, 'role': role})

        df_pickup = pd.read_excel('import/Пункты выдачи_import.xlsx', header=None, names=['address'])
        for addr in df_pickup['address']:
            PickupPoint.objects.get_or_create(address=addr)

        df_orders = pd.read_excel('import/Заказ_import.xlsx')
        for idx, row in df_orders.iterrows():
            items_str = row['Артикул заказа']
            items_list = []
            parts = [p.strip() for p in items_str.split(',')]
            for i in range(0, len(parts), 2):
                article = parts[i]
                qty = int(parts[i+1])
                try:
                    product = Product.objects.get(article=article)
                    items_list.append((product, qty))
                except Product.DoesNotExist:
                    continue

            if not items_list:
                continue

            try:
                client_profile = Profile.objects.get(full_name=row['ФИО авторизированного клиента'], role='client')
            except Profile.DoesNotExist:
                client_profile = Profile.objects.filter(role='client').first()
                if not client_profile:
                    continue

            pickup_point_id = int(row['Адрес пункта выдачи'])
            try:
                pickup_point = PickupPoint.objects.get(id=pickup_point_id)
            except PickupPoint.DoesNotExist:
                pickup_point = PickupPoint.objects.first()
                if not pickup_point:
                    continue

            order_date = row['Дата заказа']
            if isinstance(order_date, str) and order_date == '30.02.2023':
                order_date = datetime(2023, 3, 2).date()
            elif isinstance(order_date, datetime):
                order_date = order_date.date()
            else:
                order_date = datetime.now().date()

            delivery_date = row['Дата доставки']
            if isinstance(delivery_date, datetime):
                delivery_date = delivery_date.date()
            else:
                delivery_date = order_date

            order, created = Order.objects.get_or_create(
                order_number=int(row['Номер заказа']),
                defaults={
                    'order_date': order_date,
                    'delivery_date': delivery_date,
                    'pickup_point': pickup_point,
                    'client': client_profile,
                    'pickup_code': str(row['Код для получения']),
                    'status': 'new' if row['Статус заказа'] == 'Новый' else 'completed',
                }
            )
            for product, qty in items_list:
                OrderItem.objects.get_or_create(order=order, product=product, defaults={'quantity': qty})

        self.stdout.write(self.style.SUCCESS('Импорт завершён'))