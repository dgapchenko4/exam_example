from django.db import models
from django.contrib.auth.models import User

class OrderStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название статуса")
    
    class Meta:
        app_label = 'orders'
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказов"
    
    def __str__(self):
        return self.name

class PickupPoint(models.Model):
    address = models.CharField(max_length=200, verbose_name="Адрес")
    
    class Meta:
        app_label = 'orders'
        verbose_name = "Пункт выдачи"
        verbose_name_plural = "Пункты выдачи"
    
    def __str__(self):
        return self.address

class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True, verbose_name="Номер заказа")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент")
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, verbose_name="Статус")
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.PROTECT, verbose_name="Пункт выдачи")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    delivery_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата доставки")
    
    class Meta:
        app_label = 'orders'
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-order_date']
    
    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    # ИСПРАВИТЬ: 'products.Product', а не 'products.Product'
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    
    class Meta:
        app_label = 'orders'
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"
        # Можно раскомментировать, когда всё заработает:
        # unique_together = ['order', 'product']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        return self.quantity * self.price
