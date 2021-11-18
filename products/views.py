"""
views for product utilities
"""


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

    return render(request, 'products/search.html', context=context)


def product(request):
    ''' view that shows product details '''
    req = request.GET['id']
    context = {}
    try:
        product = Product.objects.get(id=req)
    except:
        messages.add_message(request, messages.ERROR, "product not found")
        return render(request, 'products/index.html', status=404)
    context['product'] = {
        'name': product.name,
        'category': product.category.name,
        'off_link': product.off_link,
        'nutriscore': product.nutriscore,
        'energy_unit': product.energy_unit,
        'energy': product.energy_100g,
        'carbohydrates': product.carbohydrates_100g,
        'sugars': product.sugars_100g,
        'fat': product.fat_100g,
        'saturated_fat': product.saturated_fat_100g,
        'fiber': product.fiber_100g,
        'proteins': product.proteins_100g,
        'salt': product.salt_100g,
        'sodium': product.sodium_100g,
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
    return redirect(f'product/?id={product.id}')


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
