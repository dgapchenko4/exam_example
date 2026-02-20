from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from .models import Product, Supplier, Order, OrderItem, Profile
from .forms import ProductForm, OrderForm, OrderItemFormSet
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
# ---- Декораторы для проверки ролей ----
def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'admin'

def is_manager_or_admin(user):
    return hasattr(user, 'profile') and user.profile.role in ['manager', 'admin']

class AdminRequiredMixin:
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_admin))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ManagerOrAdminRequiredMixin:
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_manager_or_admin))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# ---- Аутентификация ----
class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True

# ---- Список товаров ----
def product_list(request):
    template = 'main/product_list.html'
    products = Product.objects.all().select_related('category', 'supplier', 'manufacturer')
    context = {'products': products}
    if request.user.is_authenticated:
        try:
            role = request.user.profile.role
        except Profile.DoesNotExist:
            role = None
        if role in ['manager', 'admin']:
            context['show_filters'] = True
    return render(request, template, context)

def product_table_partial(request):
    products = Product.objects.all().select_related('category', 'supplier', 'manufacturer')
    search = request.GET.get('search', '')
    discount_range = request.GET.get('discount_range', '')
    sort = request.GET.get('sort', '')

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(article__icontains=search) |
            Q(description__icontains=search) |
            Q(category__name__icontains=search) |
            Q(supplier__name__icontains=search) |
            Q(manufacturer__name__icontains=search)
        )
    if discount_range:
        if discount_range == '0-11.99':
            products = products.filter(discount__lt=12)
        elif discount_range == '12-18.99':
            products = products.filter(discount__gte=12, discount__lt=19)
        elif discount_range == '19+':
            products = products.filter(discount__gte=19)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    elif sort == 'quantity_asc':
        products = products.order_by('quantity_in_stock')
    elif sort == 'quantity_desc':
        products = products.order_by('-quantity_in_stock')

    return render(request, 'main/partials/product_table.html', {'products': products})

@require_POST
@login_required
@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if OrderItem.objects.filter(product=product).exists():
        messages.error(request, 'Нельзя удалить товар, присутствующий в заказах.')
    else:
        product.delete()
        messages.success(request, 'Товар успешно удалён.')
    return redirect('product_list')

# ---- CRUD товаров (только для администратора) ----
class ProductCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    success_url = reverse_lazy('product_list')
    success_message = "Товар успешно добавлен"

class ProductUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    success_url = reverse_lazy('product_list')
    success_message = "Товар успешно изменён"

"""class ProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
    template_name = 'main/product_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if OrderItem.objects.filter(product=self.object).exists():
            messages.error(request, 'Нельзя удалить товар, присутствующий в заказах.')
            return redirect('product_list')
        return super().dispatch(request, *args, **kwargs)"""

# ---- Заказы ----
class OrderListView(ManagerOrAdminRequiredMixin, ListView):
    model = Order
    template_name = 'main/order_list.html'
    context_object_name = 'orders'
    ordering = ['-order_date']

class OrderCreateView(AdminRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'main/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = OrderItemFormSet(self.request.POST)
        else:
            data['formset'] = OrderItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Заказ создан')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class OrderUpdateView(AdminRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'main/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            data['formset'] = OrderItemFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Заказ обновлён')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class OrderDeleteView(AdminRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')
    template_name = 'main/order_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Заказ удалён')
        return super().delete(request, *args, **kwargs)