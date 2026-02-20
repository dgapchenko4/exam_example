"""
Команда для генерации варианта проекта для студента.
Использование: python manage.py generate_variant <номер_варианта>
"""
import os
import shutil
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pathlib import Path
import sys


class Command(BaseCommand):
    help = 'Генерирует вариант проекта для студента'

    def add_arguments(self, parser):
        parser.add_argument('variant_number', type=int, help='Номер варианта (1-30)')
        parser.add_argument(
            '--output-dir',
            type=str,
            default=None,
            help='Директория для вывода (по умолчанию: variant_<номер>)'
        )

    def handle(self, *args, **options):
        variant_number = options['variant_number']
        output_dir = options['output_dir'] or f'variant_{variant_number:02d}'
        
        # Получаем конфигурацию варианта
        try:
            variant = self.get_variant(variant_number)
        except ValueError as e:
            raise CommandError(str(e))
        except ImportError as e:
            raise CommandError(f'Ошибка импорта конфигурации: {e}')

        self.stdout.write(self.style.SUCCESS(f'Генерация варианта {variant_number}: {variant["theme"]}'))
        
        # Определяем пути
        base_dir = Path(__file__).resolve().parent.parent.parent.parent  # exam_example/
        variant_path = base_dir.parent / output_dir
        
        # Проверяем существование директории
        if variant_path.exists():
            self.stdout.write(self.style.WARNING(f'Директория {output_dir} уже существует. Удаление...'))
            try:
                shutil.rmtree(variant_path)
            except PermissionError:
                raise CommandError(f'Нет прав на удаление {output_dir}. Закройте файлы в этой папке.')
        
        # Создаем директорию
        try:
            variant_path.mkdir(parents=True)
            self.stdout.write(f'Создана директория: {output_dir}')
        except PermissionError:
            raise CommandError(f'Нет прав на создание директории {output_dir}')
        
        # Копируем структуру проекта
        self.stdout.write('Копирование файлов проекта...')
        copied_files = self._copy_project_structure(base_dir, variant_path)
        self.stdout.write(f'Скопировано файлов: {copied_files}')
        
        # Генерируем файлы с учетом варианта
        self.stdout.write('Генерация файлов варианта...')
        self._generate_variant_files(variant_path, variant, variant_number)
        
        # Создаем файл с информацией о варианте
        self._create_variant_info(variant_path, variant, variant_number)
        
        # Создаем файл-отчет о генерации
        self._create_generation_report(variant_path, variant_number, copied_files)
        
        self.stdout.write(self.style.SUCCESS(f'\nВариант успешно создан в директории: {output_dir}'))
        self.stdout.write(f'Тематика: {variant["theme"]}')
        self.stdout.write(f'\nСледующие шаги:')
        self.stdout.write(f'   1. cd {output_dir}')
        self.stdout.write(f'   2. python -m venv venv')
        self.stdout.write(f'   3. source venv/bin/activate  # или venv\\Scripts\\activate для Windows')
        self.stdout.write(f'   4. pip install -r requirements.txt')
        self.stdout.write(f'   5. python manage.py migrate')
        self.stdout.write(f'   6. python manage.py createsuperuser')
        self.stdout.write(f'   7. python manage.py runserver')

    def get_variant(self, variant_number):
        """Получает конфигурацию варианта"""
        # Пытаемся импортировать разными способами
        try:
            # Прямой импорт
            from variants_config import get_variant
            return get_variant(variant_number)
        except ImportError:
            try:
                # Импорт с добавлением пути
                base_dir = Path(__file__).resolve().parent.parent.parent.parent
                sys.path.insert(0, str(base_dir))
                from variants_config import get_variant
                return get_variant(variant_number)
            except ImportError:
                # Если файла нет, используем встроенную конфигурацию
                return self.get_default_variant(variant_number)

    def get_default_variant(self, variant_number):
        """Встроенная конфигурация вариантов на случай отсутствия variants_config.py"""
        variants = {
            1: {
                'theme': 'Книжный магазин',
                'main_model': 'Book',
                'main_model_verbose': 'Книга',
                'main_model_plural': 'Книги',
                'category_model': 'Genre',
                'category_verbose': 'Жанр',
                'category_plural': 'Жанры',
                'manufacturer_model': 'Publisher',
                'manufacturer_verbose': 'Издательство',
                'manufacturer_plural': 'Издательства',
                'supplier_model': 'Supplier',
                'supplier_verbose': 'Поставщик',
                'supplier_plural': 'Поставщики',
                'unit_model': 'Unit',
                'site_name': 'Книжный магазин',
                'site_title': 'Система управления книгами',
                'nav_products': 'Книги',
                'nav_orders': 'Заказы',
                'page_title_list': 'Список книг',
                'button_add': 'Добавить книгу',
            },
            2: {
                'theme': 'Магазин электроники',
                'main_model': 'Product',
                'main_model_verbose': 'Товар',
                'main_model_plural': 'Товары',
                'category_model': 'Category',
                'category_verbose': 'Категория',
                'category_plural': 'Категории',
                'manufacturer_model': 'Brand',
                'manufacturer_verbose': 'Бренд',
                'manufacturer_plural': 'Бренды',
                'supplier_model': 'Supplier',
                'supplier_verbose': 'Поставщик',
                'supplier_plural': 'Поставщики',
                'unit_model': 'Unit',
                'site_name': 'Магазин электроники',
                'site_title': 'Система управления товарами',
                'nav_products': 'Товары',
                'nav_orders': 'Заказы',
                'page_title_list': 'Каталог товаров',
                'button_add': 'Добавить товар',
            },
            3: {
                'theme': 'Медицинский центр',
                'main_model': 'Doctor',
                'main_model_verbose': 'Врач',
                'main_model_plural': 'Врачи',
                'category_model': 'Specialization',
                'category_verbose': 'Специализация',
                'category_plural': 'Специализации',
                'manufacturer_model': 'Clinic',
                'manufacturer_verbose': 'Клиника',
                'manufacturer_plural': 'Клиники',
                'supplier_model': 'Supplier',
                'supplier_verbose': 'Поставщик',
                'supplier_plural': 'Поставщики',
                'unit_model': 'Unit',
                'site_name': 'Медицинский центр',
                'site_title': 'Система записи к врачам',
                'nav_products': 'Врачи',
                'nav_orders': 'Записи',
                'page_title_list': 'Наши врачи',
                'button_add': 'Добавить врача',
            },
        }
        
        if variant_number not in variants:
            available = ', '.join(str(k) for k in variants.keys())
            raise ValueError(f'Вариант {variant_number} не найден. Доступны: {available}')
        
        return variants[variant_number]

    def _copy_project_structure(self, source, destination):
        """Копирует структуру проекта, исключая ненужные файлы"""
        exclude_dirs = {
            '__pycache__', '.git', 'venv', 'env', 'ENV',
            'media', 'staticfiles', '.vscode', '.idea',
            'migrations',  # не копируем миграции, они создадутся заново
        }
        exclude_files = {
            '.pyc', '.pyo', '.pyd', '.db', '.sqlite3',
            '.log', '.pid', '.bak', '.swp', '.swo',
            'generate_variant.py',  # не копируем сам себя
        }
        
        copied_count = 0
        
        for root, dirs, files in os.walk(source):
            # Фильтруем директории
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            # Определяем относительный путь
            rel_path = os.path.relpath(root, source)
            if rel_path == '.':
                dest_dir = destination
            else:
                dest_dir = destination / rel_path
            
            # Создаем директорию
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # Копируем файлы
            for file in files:
                # Проверяем расширение
                if any(file.endswith(ext) for ext in exclude_files):
                    continue
                
                # Проверяем точное совпадение имени
                if file in exclude_files:
                    continue
                
                src_file = Path(root) / file
                dst_file = dest_dir / file
                
                try:
                    shutil.copy2(src_file, dst_file)
                    copied_count += 1
                except (PermissionError, shutil.Error) as e:
                    self.stdout.write(self.style.WARNING(f'Не удалось скопировать {file}: {e}'))
        
        return copied_count

    def _generate_variant_files(self, variant_path, variant, variant_number):
        """Генерирует файлы с учетом варианта"""
        # Обновляем models.py
        self._update_models(variant_path, variant)
        
        # Обновляем шаблоны
        self._update_templates(variant_path, variant)
        
        # Обновляем views.py
        self._update_views(variant_path, variant)
        
        # Обновляем admin.py
        self._update_admin(variant_path, variant)
        
        # Создаем пустой __init__.py в migrations, если нужно
        migrations_dir = variant_path / 'products' / 'migrations'
        migrations_dir.mkdir(exist_ok=True)
        init_file = migrations_dir / '__init__.py'
        if not init_file.exists():
            init_file.touch()

    def _update_models(self, variant_path, variant):
        """Обновляет models.py с учетом варианта"""
        models_file = variant_path / 'products' / 'models.py'
        if not models_file.exists():
            self.stdout.write(self.style.WARNING('Файл models.py не найден'))
            return
            
        try:
            content = models_file.read_text(encoding='utf-8')
            
            # Заменяем названия моделей
            replacements = {
                'class Product': f'class {variant["main_model"]}',
                'class Category': f'class {variant["category_model"]}',
                'class Brand': f'class {variant["manufacturer_model"]}',
                'class Supplier': f'class {variant["supplier_model"]}',
                'class Unit': f'class {variant["unit_model"]}',
                
                # Verbose names
                'verbose_name="Товар"': f'verbose_name="{variant["main_model_verbose"]}"',
                'verbose_name_plural="Товары"': f'verbose_name_plural="{variant["main_model_plural"]}"',
                'verbose_name="Категория"': f'verbose_name="{variant["category_verbose"]}"',
                'verbose_name_plural="Категории"': f'verbose_name_plural="{variant["category_plural"]}"',
                'verbose_name="Бренд"': f'verbose_name="{variant["manufacturer_verbose"]}"',
                'verbose_name_plural="Бренды"': f'verbose_name_plural="{variant["manufacturer_plural"]}"',
                'verbose_name="Поставщик"': f'verbose_name="{variant["supplier_verbose"]}"',
                'verbose_name_plural="Поставщики"': f'verbose_name_plural="{variant["supplier_plural"]}"',
                
                # Имена в коде
                'Product.': f'{variant["main_model"]}.',
                'Category.': f'{variant["category_model"]}.',
                'Brand.': f'{variant["manufacturer_model"]}.',
                'Supplier.': f'{variant["supplier_model"]}.',
                'Unit.': f'{variant["unit_model"]}.',
            }
            
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            models_file.write_text(content, encoding='utf-8')
            self.stdout.write(f'models.py обновлен')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Ошибка при обновлении models.py: {e}'))

    def _update_templates(self, variant_path, variant):
        """Обновляет шаблоны с учетом варианта"""
        templates_dir = variant_path / 'templates'
        if not templates_dir.exists():
            return
        
        # Обновляем все HTML файлы
        for html_file in templates_dir.rglob('*.html'):
            try:
                content = html_file.read_text(encoding='utf-8')
                
                # Замены для всех шаблонов
                replacements = {
                    'Магазин обуви': variant['site_name'],
                    'Система управления товарами': variant['site_title'],
                    'Товары': variant['nav_products'],
                    'Заказы': variant['nav_orders'],
                    'Список товаров': variant['page_title_list'],
                    'Добавить товар': variant['button_add'],
                }
                
                for old, new in replacements.items():
                    content = content.replace(old, new)
                
                html_file.write_text(content, encoding='utf-8')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Ошибка при обновлении {html_file.name}: {e}'))
        
        self.stdout.write(f'Шаблоны обновлены')

    def _update_views(self, variant_path, variant):
        """Обновляет views.py с учетом варианта"""
        views_file = variant_path / 'products' / 'views.py'
        if not views_file.exists():
            self.stdout.write(self.style.WARNING('Файл views.py не найден'))
            return
            
        try:
            content = views_file.read_text(encoding='utf-8')
            
            # Заменяем имена моделей
            replacements = {
                'Product': variant['main_model'],
                'Category': variant['category_model'],
                'Brand': variant['manufacturer_model'],
                'Supplier': variant['supplier_model'],
                'Unit': variant['unit_model'],
            }
            
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            views_file.write_text(content, encoding='utf-8')
            self.stdout.write(f'views.py обновлен')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Ошибка при обновлении views.py: {e}'))

    def _update_admin(self, variant_path, variant):
        """Обновляет admin.py с учетом варианта"""
        admin_file = variant_path / 'products' / 'admin.py'
        if not admin_file.exists():
            return
            
        try:
            content = admin_file.read_text(encoding='utf-8')
            
            # Заменяем имена моделей
            replacements = {
                'Product': variant['main_model'],
                'Category': variant['category_model'],
                'Brand': variant['manufacturer_model'],
                'Supplier': variant['supplier_model'],
                'Unit': variant['unit_model'],
            }
            
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            admin_file.write_text(content, encoding='utf-8')
            self.stdout.write(f'admin.py обновлен')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Ошибка при обновлении admin.py: {e}'))

    def _create_variant_info(self, variant_path, variant, variant_number):
        """Создает файл с информацией о варианте"""
        info_file = variant_path / 'VARIANT_INFO.txt'
        info_content = f"""

Номер варианта: {variant_number}
Тематика: {variant['theme']}
Дата генерации: {__import__('datetime').datetime.now().strftime('%d.%m.%Y %H:%M')}

- {variant['main_model']} ({variant['main_model_verbose']})
- {variant['category_model']} ({variant['category_verbose']})
- {variant['manufacturer_model']} ({variant['manufacturer_verbose']})
- {variant['supplier_model']} ({variant['supplier_verbose']})

"""
        info_file.write_text(info_content, encoding='utf-8')
        self.stdout.write(f'VARIANT_INFO.txt создан')

    def _create_generation_report(self, variant_path, variant_number, copied_files):
        """Создает отчет о генерации"""
        report_file = variant_path / 'GENERATION_REPORT.txt'
        report_content = f"""ОТЧЕТ О ГЕНЕРАЦИИ ВАРИАНТА

Вариант: {variant_number}
Время генерации: {__import__('datetime').datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
Скопировано файлов: {copied_files}

"""
        report_file.write_text(report_content, encoding='utf-8')
