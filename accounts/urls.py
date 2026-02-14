from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),  # Путь для /login/ (без префикса)
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]