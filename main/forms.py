from django import forms
from django.forms import inlineformset_factory
from .models import Product, Order, OrderItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_number', 'order_date', 'delivery_date', 'pickup_point',
                  'client', 'pickup_code', 'status']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, fields=('product', 'quantity'),
    extra=1, can_delete=True,
    widgets={'product': forms.Select(attrs={'class': 'product-select'})}
)