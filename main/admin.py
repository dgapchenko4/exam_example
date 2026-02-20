from django.contrib import admin
from .models import Category, Manufacturer, Supplier, Product, Profile, PickupPoint, Order, OrderItem

admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(PickupPoint)
admin.site.register(Order)
admin.site.register(OrderItem)