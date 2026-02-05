from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Genre(models.Model):
    """Жанр книги"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название жанра")
    description = models.TextField(blank=True, default='', verbose_name='Описание')
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    """Автор книги"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Имя автора")
    bio = models.TextField(blank=True, verbose_name="Биография")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Publisher(models.Model):
    """Издательство"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название издательства")
    address = models.TextField(blank=True, verbose_name="Адрес")

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Книга"""
    name = models.CharField(max_length=200, verbose_name="Название книги")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Жанр")
    description = models.TextField(blank=True, verbose_name="Описание")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name="Издательство")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Цена"
    )
    year = models.IntegerField(
        verbose_name="Год издания",
        null=True,
        blank=True
    )
    pages = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Количество страниц"
    )
    isbn = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="ISBN"
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Скидка (%)"
    )
    image = models.ImageField(
        upload_to='books/',
        blank=True,
        null=True,
        verbose_name="Обложка книги"
    )
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Количество на складе"
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        """Расчетная цена с учетом скидки"""
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    @property
    def is_available(self):
        """Проверка доступности книги"""
        return self.quantity > 0

