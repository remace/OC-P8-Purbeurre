"""purbeurre URL Configuration """
from django.urls import path

from products import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('search/', views.search, name='search'),
    path('product/', views.product_view, name='product'),
    path('find-alternatives/', views.find_alternatives, name='find-alternatives'),
    path('toggle-favourite/', views.toggle_favourite, name='toggle-favourite'),
    path('list-favourites/', views.list_favourites, name='list-favourites')
]
