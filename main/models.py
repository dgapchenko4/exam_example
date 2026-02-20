from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from PIL import Image
import os

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Product(models.Model):
    article = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                 validators=[MinValueValidator(0)])
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    discount = models.IntegerField(default=0)
    quantity_in_stock = models.IntegerField(default=0,
                                            validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='products/', blank=True, null=True)

    def discounted_price(self):
        return self.price * (100 - self.discount) / 100

    def save(self, *args, **kwargs):
        try:
            this = Product.objects.get(id=self.id)
            if this.photo and this.photo != self.photo:
                if os.path.isfile(this.photo.path):
                    os.remove(this.photo.path)
        except Product.DoesNotExist:
            pass
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            if img.size != (300, 200):
                img = img.resize((300, 200), Image.Resampling.LANCZOS)
                img.save(self.photo.path)

    def clean(self):
        if self.discount < 0 or self.discount > 100:
            raise ValidationError('Скидка должна быть от 0 до 100')
        if self.price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        if self.quantity_in_stock < 0:
            raise ValidationError('Количество не может быть отрицательным')

class Profile(models.Model):
    ROLE_CHOICES = [
        ('client', 'Авторизированный клиент'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                 related_name='profile')
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')

class PickupPoint(models.Model):
    address = models.CharField(max_length=300, unique=True)

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('completed', 'Завершен'),
    ]
    order_number = models.IntegerField(unique=True)
    order_date = models.DateField()
    delivery_date = models.DateField()
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.PROTECT)
    client = models.ForeignKey(Profile, on_delete=models.PROTECT,
                               limit_choices_to={'role': 'client'})
    pickup_code = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])



