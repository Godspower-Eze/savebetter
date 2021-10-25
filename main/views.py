from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import UserCreationForm, UserLogin


def home_page(request):
    context = {

    }
    return render(request, 'index.html', context)


def login_view(request):
    form = UserLogin()

    if request.method == "POST":
        form = UserLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home_page')
    context = {
        "form": form,
        "title": "Login - SaveBetter"
    }
    return render(request, 'login.html', context)


def register_view(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            messages.success(request, 'Account created successfully. You can now login!')
            return redirect('login_view')
    context = {
        "form": form,
        "title": "Register - SaveBetter"
    }
    return render(request, 'register.html', context)
