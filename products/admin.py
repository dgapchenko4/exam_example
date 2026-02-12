from django.contrib import admin
from .models import Publisher, Product, Brand, Manufacturer, Supplier, Unit, Category

admin.site.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    ...

admin.site.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    ...

admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ...

admin.site.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation']

admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...

admin.site.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
