# shoe_store/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clinic.urls')),# Главная страница - список врачей
    path('', include('accounts.urls')),
    path('login/', include('accounts.urls')),      # Все URL-ы accounts (login, logout, register)
    path('register/', include('accounts.urls')),
    path('logout/', include('accounts.urls')),
    path('clinic/', include('clinic.urls')),       # Все URL-ы clinic с префиксом clinic/
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
