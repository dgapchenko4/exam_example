from django.contrib import admin
from .models import Order, OrderItem, OrderStatus, PickupPoint

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'status', 'order_date', 'delivery_date']
    list_filter = ['status', 'order_date']
    search_fields = ['order_number', 'customer__username']
    inlines = [OrderItemInline]
    date_hierarchy = 'order_date'

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['name']  # Только name, description нет
    search_fields = ['name']

@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ['address']  # Только address, phone нет
    search_fields = ['address']
