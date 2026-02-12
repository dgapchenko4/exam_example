import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')
django.setup()

from products.models import Unit, Brand, Supplier, Book

def clear_data():
    """Очистка данных"""
    Book.objects.all().delete()
    Unit.objects.all().delete()
    Brand.objects.all().delete()
    Supplier.objects.all().delete()
    print("Данные очищены")

def create_genres():
    """Создание жанров"""
    genres = [
        {"name": "Фантастика"},
        {"name": "Фэнтези"},
        {"name": "Детектив"},
        {"name": "Роман"},
        {"name": "Приключения"},
        {"name": "Научная литература"},
        {"name": "Биография"},
        {"name": "История"},
        {"name": "Психология"},
        {"name": "Поэзия"},
    ]
    
    for genre_data in genres:
        genre, created = Unit.objects.get_or_create(
            name=genre_data["name"]
        )
        if created:
            print(f"✓ Создан жанр: {genre_data['name']}")
        else:
            print(f"↻ Жанр уже существует: {genre_data['name']}")

def create_authors():
    """Создание авторов"""
    authors = [
        {"name": "Джордж Оруэлл"},
        {"name": "Агата Кристи"},
        {"name": "Лев Толстой"},
        {"name": "Михаил Булгаков"},
        {"name": "Фёдор Достоевский"},
        {"name": "Эрнест Хемингуэй"},
        {"name": "Джоан Роулинг"},
        {"name": "Стивен Кинг"},
        {"name": "Айзек Азимов"},
        {"name": "Рэй Брэдбери"},
    ]
    
    for author_data in authors:
        author, created = Brand.objects.get_or_create(
            name=author_data["name"]
        )
        if created:
            print(f"Создан автор: {author_data['name']}")

def create_publishers():
    """Создание издательств"""
    publishers = [
        {"name": "Эксмо"},
        {"name": "АСТ"},
        {"name": "Питер"},
        {"name": "Манн, Иванов и Фербер"},
        {"name": "Альпина Паблишер"},
        {"name": "Росмэн"},
        {"name": "Дрофа"},
        {"name": "Просвещение"},
    ]
    
    for publisher_data in publishers:
        publisher, created = Supplier.objects.get_or_create(
            name=publisher_data["name"]
        )
        if created:
            print(f"✓ Создано издательство: {publisher_data['name']}")

def create_books():
    """Создание книг"""
    # Получаем объекты
    try:
        fantasy = Unit.objects.get(name='Фантастика')
        detective = Unit.objects.get(name='Детектив')
        roman = Unit.objects.get(name='Роман')
        fantasy_genre = Unit.objects.get(name='Фэнтези')
        
        orwell = Brand.objects.get(name='Джордж Оруэлл')
        christie = Brand.objects.get(name='Агата Кристи')
        tolstoy = Brand.objects.get(name='Лев Толстой')
        bulgakov = Brand.objects.get(name='Михаил Булгаков')
        dostoevsky = Brand.objects.get(name='Фёдор Достоевский')
        hemingway = Brand.objects.get(name='Эрнест Хемингуэй')
        
        exmo = Supplier.objects.get(name='Эксмо')
        ast = Supplier.objects.get(name='АСТ')
        piter = Supplier.objects.get(name='Питер')
        mif = Supplier.objects.get(name='Манн, Иванов и Фербер')
    except Exception as e:
        print(f"Ошибка при получении объектов: {e}")
        return

    # Создаем книги
    books = [
        {
            'name': '1984',
            'description': 'Роман-антиутопия Джорджа Оруэлла о тоталитарном обществе',
            'price': 450.00,
            'quantity': 25,
            'year': 1949,
            'genre': fantasy,
            'author': orwell,
            'publisher': exmo,
        },
        {
            'name': 'Убийство в Восточном экспрессе',
            'description': 'Знаменитый детектив Агаты Кристи о расследовании убийства в поезде',
            'price': 380.00,
            'quantity': 15,
            'year': 1934,
            'genre': detective,
            'author': christie,
            'publisher': ast,
        },
        {
            'name': 'Война и мир',
            'description': 'Роман-эпопея Льва Толстого о жизни русского общества во время войны 1812 года',
            'price': 890.00,
            'quantity': 30,
            'year': 1869,
            'genre': roman,
            'author': tolstoy,
            'publisher': exmo,
        },
        {
            'name': 'Мастер и Маргарита',
            'description': 'Мистический роман Михаила Булгакова о дьяволе, посетившем Москву',
            'price': 520.00,
            'quantity': 20,
            'year': 1967,
            'genre': fantasy_genre,
            'author': bulgakov,
            'publisher': ast,
        },
        {
            'name': 'Преступление и наказание',
            'description': 'Роман Фёдора Достоевского о моральных дилеммах и раскаянии',
            'price': 410.00,
            'quantity': 18,
            'year': 1866,
            'genre': roman,
            'author': dostoevsky,
            'publisher': piter,
        },
        {
            'name': 'Старик и море',
            'description': 'Повесть Эрнеста Хемингуэя о старом рыбаке и его борьбе с большой рыбой',
            'price': 320.00,
            'quantity': 22,
            'year': 1952,
            'genre': roman,
            'author': hemingway,
            'publisher': mif,
        },
        {
            'name': 'Скотный двор',
            'description': 'Сатирическая повесть-притча Джорджа Оруэлла',
            'price': 350.00,
            'quantity': 12,
            'year': 1945,
            'genre': fantasy,
            'author': orwell,
            'publisher': exmo,
        },
        {
            'name': 'Десять негритят',
            'description': 'Детективный роман Агаты Кристи',
            'price': 390.00,
            'quantity': 17,
            'year': 1939,
            'genre': detective,
            'author': christie,
            'publisher': ast,
        },
    ]

    for book_data in books:
        book, created = Book.objects.get_or_create(
            name=book_data['name'],
            defaults=book_data
        )
        if created:
            print(f'Создана книга: {book_data["name"]} - {book_data["price"]} руб.')
        else:
            print(f'Книга уже существует: {book_data["name"]}')

if __name__ == '__main__':
    print('=' * 50)
    print('Создание тестовых данных для книжного магазина...')
    print('=' * 50)
    
    clear_data()
    create_genres()
    print('\n' + '-' * 50)
    create_authors()
    print('\n' + '-' * 50)
    create_publishers()
    print('\n' + '-' * 50)
    create_books()
    
    print('\n' + '=' * 50)
    print('Готово! Создано:')
    print(f'  Жанров: {Unit.objects.count()}')
    print(f'  Брендов: {Brand.objects.count()}')
    print(f'  Издательств: {Supplier.objects.count()}')
    print(f'  Книг: {Book.objects.count()}')
    print('=' * 50)
