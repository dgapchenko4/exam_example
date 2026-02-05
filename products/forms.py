from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """Форма для создания/редактирования книги"""

    class Meta:
        model = Book
        fields = [
            'name', 'genre', 'description', 'author',
            'publisher', 'price', 'year', 'pages', 'isbn', 'discount', 'image', 'quantity'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем подсказки к полям
        self.fields['price'].help_text = 'Цена в рублях'
        self.fields['discount'].help_text = 'Скидка в процентах (0-100)'
        self.fields['isbn'].help_text = 'Международный стандартный книжный номер (13 цифр)'