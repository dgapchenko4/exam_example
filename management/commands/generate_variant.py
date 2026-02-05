"""
Команда для генерации варианта проекта для студента.
Использование: python manage.py generate_variant <номер_варианта>
"""
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import sys

# Добавляем корневую директорию в путь для импорта
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

try:
    from variants_config import get_variant
except ImportError:
    # Если импорт не работает, пробуем другой путь
    sys.path.insert(0, str(BASE_DIR))
    from variants_config import get_variant


class Command(BaseCommand):
    help = 'Генерирует вариант проекта для студента'

    def add_arguments(self, parser):
        parser.add_argument('variant_number', type=int, help='Номер варианта (1-6)')
        parser.add_argument(
            '--output-dir',
            type=str,
            default=None,
            help='Директория для вывода (по умолчанию: variant_<номер>)'
        )

    def handle(self, *args, **options):
        variant_number = options['variant_number']
        output_dir = options['output_dir'] or f'variant_{variant_number}'
        
        try:
            variant = get_variant(variant_number)
        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return

        self.stdout.write(self.style.SUCCESS(f'Генерация варианта {variant_number}: {variant["theme"]}'))
        
        # Создаем директорию для варианта
        variant_path = BASE_DIR.parent / output_dir
        if variant_path.exists():
            self.stdout.write(self.style.WARNING(f'Директория {output_dir} уже существует. Удаление...'))
            shutil.rmtree(variant_path)
        
        variant_path.mkdir(parents=True)
        
        # Копируем структуру проекта
        self.stdout.write('Копирование файлов проекта...')
        self._copy_project_structure(BASE_DIR, variant_path)
        
        # Генерируем файлы с учетом варианта
        self.stdout.write('Генерация файлов варианта...')
        self._generate_variant_files(variant_path, variant, variant_number)
        
        # Создаем файл с информацией о варианте
        self._create_variant_info(variant_path, variant, variant_number)
        
        self.stdout.write(self.style.SUCCESS(f'\nВариант успешно создан в директории: {output_dir}'))
        self.stdout.write(f'Тематика: {variant["theme"]}')
        self.stdout.write(f'\nСледующие шаги:')
        self.stdout.write(f'1. cd {output_dir}')
        self.stdout.write(f'2. python manage.py migrate')
        self.stdout.write(f'3. python manage.py populate_db')
        self.stdout.write(f'4. python manage.py runserver')

    def _copy_project_structure(self, source, destination):
        """Копирует структуру проекта, исключая ненужные файлы"""
        exclude_dirs = {'__pycache__', '.git', 'db.sqlite3', 'media', 'staticfiles', '.vscode'}
        exclude_files = {'.pyc', '.pyo', '.pdf', 'Zone.Identifier'}
        
        for root, dirs, files in os.walk(source):
            # Фильтруем директории
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            # Определяем относительный путь
            rel_path = os.path.relpath(root, source)
            if rel_path == '.':
                dest_dir = destination
            else:
                dest_dir = destination / rel_path
            
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # Копируем файлы
            for file in files:
                if any(file.endswith(ext) for ext in exclude_files):
                    continue
                if file == 'generate_variant.py':
                    continue
                    
                src_file = Path(root) / file
                dst_file = dest_dir / file
                shutil.copy2(src_file, dst_file)

    def _generate_variant_files(self, variant_path, variant, variant_number):
        """Генерирует файлы с учетом варианта"""
        # Обновляем models.py
        self._update_models(variant_path, variant)
        
        # Обновляем шаблоны
        self._update_templates(variant_path, variant)
        
        # Обновляем views.py
        self._update_views(variant_path, variant)
        
        # Обновляем forms.py
        self._update_forms(variant_path, variant)
        
        # Обновляем settings.py
        self._update_settings(variant_path, variant)

    def _update_models(self, variant_path, variant):
        """Обновляет models.py с учетом варианта"""
        models_file = variant_path / 'products' / 'models.py'
        if not models_file.exists():
            return
            
        content = models_file.read_text(encoding='utf-8')
        
        # Заменяем названия моделей и verbose_name
        replacements = {
            'class Product': f'class {variant["main_model"]}',
            'class Category': f'class {variant["category_model"]}',
            'class Manufacturer': f'class {variant["manufacturer_model"]}',
            'class Supplier': f'class {variant["supplier_model"]}',
            'class Unit': f'class {variant["unit_model"]}',
            'verbose_name="Товар"': f'verbose_name="{variant["main_model_verbose"]}"',
            'verbose_name_plural="Товары"': f'verbose_name_plural="{variant["main_model_plural"]}"',
            'verbose_name="Категория"': f'verbose_name="{variant["category_verbose"]}"',
            'verbose_name_plural="Категории"': f'verbose_name_plural="{variant["category_plural"]}"',
            'verbose_name="Производитель"': f'verbose_name="{variant["manufacturer_verbose"]}"',
            'verbose_name_plural="Производители"': f'verbose_name_plural="{variant["manufacturer_plural"]}"',
            'verbose_name="Поставщик"': f'verbose_name="{variant["supplier_verbose"]}"',
            'verbose_name_plural="Поставщики"': f'verbose_name_plural="{variant["supplier_plural"]}"',
            'Product.objects': f'{variant["main_model"]}.objects',
            'Category': variant['category_model'],
            'Manufacturer': variant['manufacturer_model'],
            'Supplier': variant['supplier_model'],
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        models_file.write_text(content, encoding='utf-8')

    def _update_templates(self, variant_path, variant):
        """Обновляет шаблоны с учетом варианта"""
        # Обновляем base.html
        base_template = variant_path / 'templates' / 'base' / 'base.html'
        if base_template.exists():
            content = base_template.read_text(encoding='utf-8')
            content = content.replace('Магазин обуви', variant['site_name'])
            content = content.replace('Система управления товарами', variant['site_title'])
            content = content.replace('Товары', variant['nav_products'])
            base_template.write_text(content, encoding='utf-8')
        
        # Обновляем product_list.html
        product_list = variant_path / 'templates' / 'products' / 'product_list.html'
        if product_list.exists():
            content = product_list.read_text(encoding='utf-8')
            content = content.replace('Список товаров', variant['page_title_list'])
            content = content.replace('Добавить товар', variant['button_add'])
            product_list.write_text(content, encoding='utf-8')

    def _update_views(self, variant_path, variant):
        """Обновляет views.py с учетом варианта"""
        views_file = variant_path / 'products' / 'views.py'
        if not views_file.exists():
            return
            
        content = views_file.read_text(encoding='utf-8')
        content = content.replace('Product', variant['main_model'])
        content = content.replace('Category', variant['category_model'])
        content = content.replace('Manufacturer', variant['manufacturer_model'])
        content = content.replace('Supplier', variant['supplier_model'])
        views_file.write_text(content, encoding='utf-8')

    def _update_forms(self, variant_path, variant):
        """Обновляет forms.py с учетом варианта"""
        forms_file = variant_path / 'products' / 'forms.py'
        if not forms_file.exists():
            return
            
        content = forms_file.read_text(encoding='utf-8')
        content = content.replace('Product', variant['main_model'])
        content = content.replace('Category', variant['category_model'])
        content = content.replace('Manufacturer', variant['manufacturer_model'])
        content = content.replace('Supplier', variant['supplier_model'])
        forms_file.write_text(content, encoding='utf-8')

    def _update_settings(self, variant_path, variant):
        """Обновляет settings.py (если нужно)"""
        pass  # Пока не требуется

    def _create_variant_info(self, variant_path, variant, variant_number):
        """Создает файл с информацией о варианте"""
        info_file = variant_path / 'VARIANT_INFO.txt'
        info_content = f"""ИНФОРМАЦИЯ О ВАРИАНТЕ ПРОЕКТА

Номер варианта: {variant_number}
Тематика: {variant['theme']}

ОСНОВНЫЕ МОДЕЛИ:
- {variant['main_model']} ({variant['main_model_verbose']})
- {variant['category_model']} ({variant['category_verbose']})
- {variant['manufacturer_model']} ({variant['manufacturer_verbose']})
- {variant['supplier_model']} ({variant['supplier_verbose']})

НАСТРОЙКИ ПРОЕКТА:
- Название сайта: {variant['site_name']}
- Заголовок: {variant['site_title']}
- Навигация: {variant['nav_products']}, {variant['nav_orders']}

ВАЖНО:
Этот вариант был автоматически сгенерирован из базового проекта.
Все модели и шаблоны адаптированы под тематику "{variant['theme']}".

Для запуска проекта:
1. python manage.py migrate
2. python manage.py populate_db
3. python manage.py runserver
"""
        info_file.write_text(info_content, encoding='utf-8')
