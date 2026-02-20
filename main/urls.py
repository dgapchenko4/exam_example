from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.product_list, name='product_list'),
    path('product_table_partial/', views.product_table_partial, name='product_table_partial'),
    
    # Маршруты для товаров
    path('product/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    # Маршруты для заказов
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order/add/', views.OrderCreateView.as_view(), name='order_add'),
    path('order/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_edit'),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
]