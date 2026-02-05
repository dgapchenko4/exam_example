from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from products.views import product_list  # Импортируем product_list
from accounts.views import register_view, custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_list, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', register_view, name='register'),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
]
