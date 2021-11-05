from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User

# Create your views here.

# create
def register(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user = User(request, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        if user is not None:
            login(request, user)
            messages.error(request, f"{user.email} logged in")
            return render(request, 'products/index.html')
        else:
            messages.error(request, "echec de l'enregistrement")
            return render(request, 'accounts/register.html')
    else:
        return render(request, 'accounts/register.html')

# read
def profile(request):

    if request.user.is_authenticated:
        pass

    return render(request, 'accounts/profile.html')

# update

# delete

# authentification views 
def login_user(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.error(request, f"{user.email} logged in")
            return render(request, 'products/index.html')
        else:
            messages.error(request, "echec de l'identification")
            return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    pass