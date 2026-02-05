from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from products.views import product_list
from accounts.views import register_view, custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_list, name='home'),
    
    # Используем встроенный LoginView
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # Используем наше кастомное представление для logout
    path('logout/', custom_logout, name='logout'),
    
    # Регистрация
    path('register/', register_view, name='register'),
]
