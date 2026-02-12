import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')
django.setup()

from products.models import Unit, Brand, Supplier, Book

def generate_isbn():
    """Генерация случайного ISBN"""
    # ISBN-13 формат: 978-XXX-XX-XXXXX-X
    prefix = "978"
    group = str(random.randint(100, 999))
    publisher = str(random.randint(10, 99))
    book_number = str(random.randint(10000, 99999))
    
    # Собираем базовый номер
    base = prefix + group + publisher + book_number
    
    # Вычисляем контрольную цифру для ISBN-13
    total = 0
    for i, digit in enumerate(base):
        if i % 2 == 0:
            total += int(digit)
        else:
            total += int(digit) * 3
    
    check_digit = (10 - (total % 10)) % 10
    
    return f"{prefix}-{group}-{publisher}-{book_number}-{check_digit}"

def clear_data():
    """Очистка данных"""
    Book.objects.all().delete()
    print("Существующие книги удалены")

def create_genres():
    """Создание жанров (если их нет)"""
    genres = [
        {"name": "Фантастика", "slug": "fantastika"},
        {"name": "Фэнтези", "slug": "fentezi"},
        {"name": "Детектив", "slug": "detektiv"},
        {"name": "Роман", "slug": "roman"},
        {"name": "Приключения", "slug": "priklyucheniya"},
        {"name": "Научная литература", "slug": "nauchnaya-literatura"},
        {"name": "Биография", "slug": "biografiya"},
        {"name": "История", "slug": "istoriya"},
        {"name": "Психология", "slug": "psihologiya"},
        {"name": "Поэзия", "slug": "poeziya"},
    ]
    
    for genre_data in genres:
        genre, created = Unit.objects.get_or_create(
            name=genre_data["name"],
            defaults={"slug": genre_data["slug"]}
        )
        if created:
            print(f"✓ Создан жанр: {genre_data['name']}")
        else:
            print(f"↻ Жанр уже существует: {genre_data['name']}")

def create_authors():
    """Создание авторов (если их нет)"""
    authors = [
        "Джордж Оруэлл",
        "Агата Кристи",
        "Лев Толстой",
        "Михаил Булгаков",
        "Фёдор Достоевский",
        "Эрнест Хемингуэй",
        "Джоан Роулинг",
        "Стивен Кинг",
        "Айзек Азимов",
        "Рэй Брэдбери",
        "Марк Твен",
        "Джек Лондон",
        "Антон Чехов",
        "Александр Пушкин",
    ]
    
    for name in authors:
        author, created = Brand.objects.get_or_create(name=name)
        if created:
            print(f"✓ Создан автор: {name}")
        else:
            print(f"↻ Бренд уже существует: {name}")

def create_publishers():
    """Создание издательств (если их нет)"""
    publishers = [
        "Эксмо",
        "АСТ",
        "Питер",
        "Манн, Иванов и Фербер",
        "Альпина Паблишер",
        "Росмэн",
        "Дрофа",
        "Просвещение",
        "Речь",
        "Corpus",
    ]
    
    for name in publishers:
        publisher, created = Supplier.objects.get_or_create(name=name)
        if created:
            print(f"✓ Создано издательство: {name}")
        else:
            print(f"↻ Производитель уже существует: {name}")

def create_all_books():
    """Создание всех книг с уникальными ISBN"""
    # Получаем жанры
    fantasy = Unit.objects.get(name='Фантастика')
    detective = Unit.objects.get(name='Детектив')
    roman = Unit.objects.get(name='Роман')
    fantasy_genre = Unit.objects.get(name='Фэнтези')
    adventure = Unit.objects.get(name='Приключения')
    science_lit = Unit.objects.get(name='Научная литература')
    biography = Unit.objects.get(name='Биография')
    history = Unit.objects.get(name='История')
    psychology = Unit.objects.get(name='Психология')
    poetry = Unit.objects.get(name='Поэзия')
    
    # Получаем или создаем авторов
    authors = {}
    author_list = [
        "Джордж Оруэлл", "Агата Кристи", "Лев Толстой", "Михаил Булгаков",
        "Фёдор Достоевский", "Эрнест Хемингуэй", "Джоан Роулинг", "Стивен Кинг",
        "Айзек Азимов", "Рэй Брэдбери", "Марк Твен", "Джек Лондон",
        "Антон Чехов", "Александр Пушкин", "Николай Гоголь", "Иван Тургенев"
    ]
    
    for name in author_list:
        authors[name], _ = Brand.objects.get_or_create(name=name)
    
    # Получаем или создаем издательства
    publishers = {}
    publisher_list = ["Эксмо", "АСТ", "Питер", "Манн, Иванов и Фербер", 
                     "Альпина Паблишер", "Росмэн", "Дрофа", "Просвещение"]
    
    for name in publisher_list:
        publishers[name], _ = Supplier.objects.get_or_create(name=name)
    
    # Список всех книг для создания
    all_books = [
        # Фантастика
        {
            'name': '1984',
            'description': 'Роман-антиутопия Джорджа Оруэлла о тоталитарном обществе',
            'price': 450.00,
            'quantity': 25,
            'year': 1949,
            'genre': fantasy,
            'author': authors['Джордж Оруэлл'],
            'publisher': publishers['Эксмо'],
            'isbn': '978-5-04-123456-7'
        },
        {
            'name': 'Скотный двор',
            'description': 'Сатирическая повесть-притча Джорджа Оруэлла',
            'price': 350.00,
            'quantity': 12,
            'year': 1945,
            'genre': fantasy,
            'author': authors['Джордж Оруэлл'],
            'publisher': publishers['АСТ'],
            'isbn': '978-5-17-123456-8'
        },
        {
            'name': 'Собачье сердце',
            'description': 'Повесть Михаила Булгакова о научном эксперименте',
            'price': 280.00,
            'quantity': 19,
            'year': 1925,
            'genre': fantasy,
            'author': authors['Михаил Булгаков'],
            'publisher': publishers['АСТ'],
            'isbn': '978-5-17-123457-9'
        },
        {
            'name': 'Я, робот',
            'description': 'Сборник рассказов Айзека Азимова о роботах',
            'price': 470.00,
            'quantity': 21,
            'year': 1950,
            'genre': fantasy,
            'author': authors['Айзек Азимов'],
            'publisher': publishers['Эксмо'],
            'isbn': '978-5-04-123458-0'
        },
        {
            'name': '451° по Фаренгейту',
            'description': 'Роман-антиутопия Рея Брэдбери о будущем, где книги запрещены',
            'price': 390.00,
            'quantity': 18,
            'year': 1953,
            'genre': fantasy,
            'author': authors['Рэй Брэдбери'],
            'publisher': publishers['АСТ'],
            'isbn': '978-5-17-123459-1'
        },
        
        # Детектив
        {
            'name': 'Убийство в Восточном экспрессе',
            'description': 'Знаменитый детектив Агаты Кристи о расследовании убийства в поезде',
            'price': 380.00,
            'quantity': 15,
            'year': 1934,
            'genre': detective,
            'author': authors['Агата Кристи'],
            'publisher': publishers['АСТ'],
            'isbn': '978-5-17-123460-7'
        },
        {
            'name': 'Десять негритят',
            'description': 'Детективный роман Агаты Кристи',
            'price': 390.00,
            'quantity': 17,
            'year': 1939,
            'genre': detective,
            'author': authors['Агата Кристи'],
            'publisher': publishers['АСТ'],
            'isbn': '978-5-17-123461-8'
        },
        
        # Роман
        {
            'name': 'Война и мир',
            'description': 'Роман-эпопея Льва Толстого о жизни русского общества во время войны 1812 года',
            'price': 890.00,
            'quantity': 30,
            'year': 1869,
            'genre': roman,
            'author': authors['Лев Толстой'],
            'publisher': publishers['Эксмо'],
            'isbn': '978-5-04-123462-4'
        },
        {
            'name': 'Анна Каренина',
            'description': 'Роман Льва Толстого о любви и обществе',
            'price': 650.00,
            'quantity': 22,
            'year': 1877,
            'genre': roman,
            'author': authors['Лев Толстой'],
            'publisher': publishers['Эксмо'],
            'isbn': '978-5-04-123463-5'
        },
        {
            'name': 'Прощай, оружие!',
            'description': 'Роман Эрнеста Хемингуэя о Первой мировой войне',
            'price': 420.00,
            'quantity': 14,
            'year': 1929,
            'genre': roman,
            'author': authors['Эрнест Хемингуэй'],
            'publisher': publishers['Манн, Иванов и Фербер'],
            'isbn': '978-5-001-12345-7'
        },
        
        # Фэнтези
        {
            'name': 'Гарри Поттер и философский камень',
            'description': 'Первая книга серии о юном волшебнике',
            'price': 550.00,
            'quantity': 35,
            'year': 1997,
            'genre': fantasy_genre,
            'author': authors['Джоан Роулинг'],
            'publisher': publishers['Эксмо'],
            'isbn': '978-5-04-123467-9'
        },
        {
            'name': 'Оно',
            'description': 'Роман ужасов Стивена Кинга о древнем зле',
            'price': 680.00,
            'quantity': 14,
            'year': 1986,
            'genre': fantasy_genre,
            'author': authors['Стивен Кинг'],
            'publisher': publishers['АСТ'],
            'isbn': '978-5-17-123468-0'
        },
        
        # Приключения
        {
            'name': 'Приключения Тома Сойера',
            'description': 'Повесть Марка Твена о приключениях мальчика в Америке XIX века',
            'price': 320.00,
            'quantity': 25,
            'year': 1876,
            'genre': adventure,
            'author': authors['Марк Твен'],
            'publisher': publishers['Питер'],
            'isbn': '978-5-4461-1235-7'
        },
        
        # Другие жанры (по 1-2 книги для теста)
        {
            'name': 'Краткая история времени',
            'description': 'Научно-популярная книга Стивена Хокинга о космологии',
            'price': 580.00,
            'quantity': 10,
            'year': 1988,
            'genre': science_lit,
            'author': Brand.objects.get_or_create(name='Стивен Хокинг')[0],
            'publisher': publishers['Альпина Паблишер'],
            'isbn': '978-5-9614-1234-8'
        },
        {
            'name': 'Евгений Онегин',
            'description': 'Роман в стихах Александра Пушкина',
            'price': 290.00,
            'quantity': 20,
            'year': 1833,
            'genre': poetry,
            'author': authors['Александр Пушкин'],
            'publisher': publishers['Дрофа'],
            'isbn': '978-5-358-12345-9'
        },
    ]
    
    created_count = 0
    for book_data in all_books:
        try:
            # Используем get_or_create с isbn
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            if created:
                print(f'✓ Создана книга: {book_data["name"]} - {book_data["price"]} руб.')
                created_count += 1
            else:
                print(f'↻ Книга уже существует: {book_data["name"]}')
        except Exception as e:
            print(f"✗ Ошибка при создании книги '{book_data['name']}': {e}")
            # Попробуем с другим ISBN
            try:
                book_data['isbn'] = generate_isbn()
                book = Book.objects.create(**book_data)
                print(f'✓ Создана книга (с новым ISBN): {book_data["name"]}')
                created_count += 1
            except Exception as e2:
                print(f"✗ Критическая ошибка для '{book_data['name']}': {e2}")
    
    return created_count

def main():
    """Основная функция - создает все данные"""
    print('=' * 60)
    print('Создание полной базы данных для книжного магазина...')
    print('=' * 60)
    
    try:
        clear_data()
        print('\n' + '-' * 60)
        create_genres()
        print('\n' + '-' * 60)
        create_authors()
        print('\n' + '-' * 60)
        create_publishers()
        print('\n' + '-' * 60)
        
        print("Создание всех книг...")
        created_books = create_all_books()
        
        print('\n' + '=' * 60)
        print('ИТОГОВАЯ СТАТИСТИКА:')
        print('=' * 60)
        print(f'  Жанров в базе: {Unit.objects.count()}')
        print(f'  Брендов в базе: {Brand.objects.count()}')
        print(f'  Издательств в базе: {Supplier.objects.count()}')
        print(f'  Всего книг в базе: {Book.objects.count()}')
        print(f'  Создано в этом запуске: {created_books} книг')
        print('=' * 60)
        
        # Покажем распределение книг по жанрам
        print("\nРаспределение книг по жанрам:")
        for genre in Unit.objects.all():
            books_count = Book.objects.filter(genre=genre).count()
            if books_count > 0:
                print(f"  {genre.name}: {books_count} книг")
        
    except Exception as e:
        print(f"\n✗ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
