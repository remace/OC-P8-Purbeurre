""" routes for accounts app """
from django.urls import path

from accounts import views

urlpatterns = [
    path('profile/', views.profile, name='profile' ),
    path('register/', views.register, name='register' ),
    path('login/', views.login_user, name='login' ),
    path('logout/', views.logout_user, name='logout' ),
]
