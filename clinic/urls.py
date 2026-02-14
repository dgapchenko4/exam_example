from django.urls import path
from . import views
from clinic.views import doctor_list
urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('services/', views.service_list, name='service_list'),
    path('appointment/new/', views.appointment_create, name='appointment_create'),
    path('appointment/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/', views.appointment_list, name='appointment_list'),
]