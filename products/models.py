# products/models.py
from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    
    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    contact_info = models.TextField(blank=True, verbose_name="Контактная информация")
    
    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    abbreviation = models.CharField(max_length=10, verbose_name="Сокращение")
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Родительская категория")
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.IntegerField(default=0, verbose_name="Количество")
    
    # Связи с другими моделями
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Издатель")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Бренд")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Поставщик")
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Единица измерения")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
