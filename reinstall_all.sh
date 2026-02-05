#!/bin/bash
echo "=== ПОЛНАЯ ПЕРЕУСТАНОВКА DJANGO ==="

# 1. Остановить сервер
echo "1. Остановка сервера..."
pkill -f "python.*manage.py runserver" 2>/dev/null || true

# 2. Удалить старый venv
echo "2. Удаление старого venv..."
rm -rf venv/

# 3. Создать новый venv
echo "3. Создание нового venv..."
python3 -m venv venv

# 4. Активировать
echo "4. Активация venv..."
source venv/bin/activate

# 5. Проверить Python
echo "5. Проверка Python:"
echo "   Путь: $(which python)"
echo "   Версия: $(python --version)"

# 6. Установить Django
echo "6. Установка Django..."
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir django==4.2.11 pillow==10.2.0

# 7. Проверить установку
echo "7. Проверка Django..."
DJANGO_VER=$(python -m django --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "   ✅ Django $DJANGO_VER установлен"
else
    echo "   ❌ Django НЕ установлен"
    exit 1
fi

# 8. Проверить файл migration.py
echo "8. Проверка файла migration.py..."
if python -c "from django.db.migrations import migration; print('   ✅ Файл импортируется')" 2>/dev/null; then
    echo "   ✅ Файл migration.py найден"
else
    echo "   ❌ Файл migration.py НЕ НАЙДЕН"
    
    # Показать что есть в папке миграций
    DJANGO_PATH=$(python -c "import django; print(django.__file__)" 2>/dev/null | sed 's/__init__.py//')
    echo "   Содержимое папки миграций:"
    ls -la "$DJANGO_PATH/db/migrations/" 2>/dev/null || echo "   Папка не найдена"
    
    # Скачать файл вручную
    echo "   Попытка скачать файл..."
    MIGRATION_URL="https://raw.githubusercontent.com/django/django/4.2.11/django/db/migrations/migration.py"
    MIGRATION_DIR="venv/lib/python3.12/site-packages/django/db/migrations"
    
    mkdir -p "$MIGRATION_DIR"
    curl -s "$MIGRATION_URL" -o "$MIGRATION_DIR/migration.py"
    
    if [ -f "$MIGRATION_DIR/migration.py" ]; then
        echo "   ✅ Файл скачан вручную"
    else
        echo "   ❌ Не удалось скачать файл"
        exit 1
    fi
fi

echo "=== ПЕРЕУСТАНОВКА ЗАВЕРШЕНА ==="
