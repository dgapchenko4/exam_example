from django.contrib import admin
from .models import Order, OrderItem, OrderStatus, PickupPoint
from products.models import Book  # Если нужно импортировать Book


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    # Исправьте product на book если нужно
    # fields = ['book', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'status', 'customer', 'order_date', 'delivery_date')
    list_filter = ('status', 'order_date')
    search_fields = ('order_number', 'customer__username')
    inlines = [OrderItemInline]


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ('address',)
    search_fields = ('address',)
