from django.contrib import admin
from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.profile, name='index' )
]