from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@require_http_methods(["GET", "POST"])
def custom_logout(request):
    """Кастомный выход, работающий с GET-запросами"""
    logout(request)
    return redirect('home')
