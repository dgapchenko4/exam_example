#!/bin/bash
echo "=== ВОССТАНОВЛЕНИЕ DJANGO ДЛЯ UBUNTU/DEBIAN ==="

# 1. Удалить старый venv
echo "Удаление старого venv..."
rm -rf venv/

# 2. Создать новый venv с python3
echo "Создание нового venv..."
python3 -m venv venv

# 3. Активировать
echo "Активация venv..."
source venv/bin/activate

# 4. Проверить Python
echo "Проверка Python:"
which python
python --version

# 5. Установить Django
echo "Установка Django..."
pip install django==4.2.11 pillow==10.2.0

# 6. Проверить установку
echo "Проверка установки..."
DJANGO_VERSION=$(python -m django --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Django установлен: версия $DJANGO_VERSION"
else
    echo "❌ Ошибка установки Django"
    exit 1
fi

# 7. Проверить файл migration.py
if find venv -name "migration.py" -type f | grep -q .; then
    echo "✅ Файл migration.py найден"
else
    echo "❌ Файл migration.py не найден"
    exit 1
fi

echo "=== ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО ==="
