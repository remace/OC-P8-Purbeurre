"""
views for product utilities
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from accounts.models import User
from .models import Product


def index(request):
    ''' view displaying the home page of the website '''
    return render(request, 'products/index.html')


def search(request):
    ''' view displaying search title-matching products'''
    req = request.GET['search']
    context = {}
    context['search'] = req

    products = Product.objects.filter(name__icontains=req).values()
    context['results'] = products
    context['page']= 'Recherche'

    return render(request, 'products/search.html', context=context)


def product(request):
    ''' view that shows product details '''
    req = request.GET['id']
    context = {}
    try:
        product = Product.objects.get(id=req)
    except Product.DoesNotExist:
        messages.add_message(request, messages.ERROR, "product not found")
        return render(request, 'products/index.html', status=404)
    context['product'] = {
        'name': product.name,
        'category': product.category.name,
        'off_link': product.off_link,
        'off_thumb_link': product.off_thumb_link,
        'off_img_link': product.off_img_link,
        'nutriscore': product.nutriscore,
        'energy_unit': product.energy_unit,
        'energy_100g': product.energy_100g,
        'carbohydrates_100g': product.carbohydrates_100g,
        'sugars_100g': product.sugars_100g,
        'fat_100g': product.fat_100g,
        'saturated_fat_100g': product.saturated_fat_100g,
        'fiber_100g': product.fiber_100g,
        'proteins_100g': product.proteins_100g,
        'salt_100g': product.salt_100g,
        'sodium_100g': product.sodium_100g,
        'id': product.id,
    }

    if request.user.is_authenticated:
        if product.in_users_favourites.all().filter(id=request.user.id):
            context['product']['is_favourite'] = True
            context['favourite_toggle_inactive'] = False
        else:
            context['product']['is_favourite'] = False
            context['favourite_toggle_inactive'] = False
    else:
        context['favourite_toggle_inactive'] = True
    return render(request, 'products/product.html', context=context)


@login_required
def toggle_favourite(request):
    ''' toggle a product as favourite of a connected user '''
    product = Product.objects.get(pk=request.POST['product_id'])
    user = request.user

    if product.in_users_favourites.all().filter(id=user.id):
        product.in_users_favourites.remove(user)
    else:
        product.in_users_favourites.add(user)
    return redirect(f'{ reverse("product") }?id={product.id}')


@login_required
def list_favourites(request):
    ''' view displaying given user's favourites list '''
    user = User.objects.get(id=request.user.id)
    products = Product.objects.filter(in_users_favourites__id=user.id)
    context={}
    context['page'] = 'Mes Favoris'
    context['results'] = products
    return render(request, 'products/search.html', context=context)


def find_alternatives(request):
    ''' view getting alternatives to a product '''
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    category = product.category
    products = Product.objects.filter(
        category=category,
        nutriscore__lte=product.nutriscore).all()

    context = {}
    context['results'] = products

    return render(request, 'products/search.html', context=context)
