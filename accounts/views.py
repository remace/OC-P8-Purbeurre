from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from validate_email import validate_email

from .models import User

def register(request):
    if request.method=='POST':
        has_error = False
        
        # get form elements
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # check integrity of data
        if not password==password2:
            messages.error(request, f"mots de passe différents")
            has_error=True
        
        if len(password) <= 6:
            messages.error(request, f"mot de passe trop court")
            has_error=True
        
        if not validate_email(email):
            messages.error(request, f"email invalide")
            has_error=True

        if User.objects.filter(email=email).exists():
            messages.error(request, f"email déjà utilisé")
            has_error=True

        # if no error from form validation
        if has_error:
            return render(request, 'accounts/register.html',status=400)
        else:
            # save the user in database
            user = User(email=email, password=password) #TODO hash password
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # then connect this user
            if user is not None:
                login(request, user)
                return redirect('products/index')
            else:
                return render(request, 'accounts/register.html')      
    else:
        # if it is a get method, render the User registration form
        return render(request, 'accounts/register.html')


def login_user(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = authenticate(request, email=email, password=password)
        except e:
            print(e)

        if user is not None:
            login(request, user)
            messages.error(request, f"{user.email} logged in")
            return render(request, 'products/index.html')
        else:
            messages.error(request, "echec de l'identification")
            return render(request, 'accounts/login.html')
    else:
        # if it is a get method, render the User login form
        return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return render(request, 'products/index.html')




# read
def profile(request):

    if request.user.is_authenticated:
        pass

    return render(request, 'accounts/profile.html')


