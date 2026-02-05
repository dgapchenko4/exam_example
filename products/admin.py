from django.contrib import admin
from .models import Genre, Book, Author, Publisher



# Register your models here.
@admin.register(Genre)
class BookAdmin(admin.ModelAdmin):
    ...

@admin.register(Book)
class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Author)
class ManufacturerAdmin(admin.ModelAdmin):
    ...
    
@admin.register(Publisher)
class SupplierAdmin(admin.ModelAdmin):
    ...
