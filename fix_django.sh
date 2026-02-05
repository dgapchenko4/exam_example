#!/bin/bash
echo "=== ВОССТАНОВЛЕНИЕ DJANGO ==="

# 1. Деактивировать venv если активирован
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Деактивация текущего venv..."
    deactivate
fi

# 2. Удалить старый venv
echo "Удаление старого venv..."
rm -rf venv/

# 3. Создать новый venv
echo "Создание нового venv..."
python -m venv venv

# 4. Активировать
echo "Активация venv..."
source venv/bin/activate

# 5. Обновить pip
echo "Обновление pip..."
pip install --upgrade pip

# 6. Установить Django
echo "Установка Django..."
pip install django==4.2.11 pillow==10.2.0

# 7. Проверить установку
echo "Проверка установки..."
DJANGO_VERSION=$(python -m django --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Django установлен: версия $DJANGO_VERSION"
else
    echo "❌ Ошибка установки Django"
    exit 1
fi

# 8. Проверить файл migration.py
if find venv -name "migration.py" -type f | grep -q .; then
    echo "✅ Файл migration.py найден"
else
    echo "❌ Файл migration.py не найден"
    exit 1
fi

echo "=== ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО ==="
