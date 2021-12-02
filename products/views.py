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


def legal_notices(request):
    '''view rendering the legal notices page of the site'''
    return render(request,'products/legal-notices.html')


def search(request):
    ''' view displaying search title-matching products'''
    req = request.GET['search']
    context = {}
    context['results'] = []
    context['search'] = req

    products = Product.objects.filter(name__icontains=req).values()
    for product in products:
        context['results'].append(product)
    users_favourite_products = []
    if request.user.is_authenticated:
        favourite_products = (Product.objects
                                .filter(in_users_favourites__id=request.user.id)
                                .values()
                                )
        for favourite_product in favourite_products:
            users_favourite_products.append(favourite_product)
    for product in context['results']:
        product['is_favourite'] = product in users_favourite_products
    context['page']= 'Recherche'
    return render(request, 'products/search.html', context=context)


def product_view(request):
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
    if request.method == 'POST':
        product_id = request.POST['product_id']
        next_page = f'{ reverse("product") }?id={product_id}'
    else:
        product_id = request.GET['product_id']
        next_page = request.GET['next_page']
        print(f'next_page: {next_page}')
        if next_page == 'search':
            search_str = request.GET['search']
            next_page= f'{ reverse("search") }?search={search_str}'
        elif next_page == 'find-alternatives':
            from_id = request.GET['from_id']
            next_page = f'{reverse("find-alternatives")}?product_id={from_id}'

    product = Product.objects.get(pk=product_id)
    user = request.user

    if product.in_users_favourites.all().filter(id=user.id):
        product.in_users_favourites.remove(user)
    else:
        product.in_users_favourites.add(user)
    return redirect(next_page)


@login_required
def list_favourites(request):
    ''' view displaying given user's favourites list '''
    user = User.objects.get(id=request.user.id)
    products = Product.objects.filter(in_users_favourites__id=user.id).values()
    context={}
    context['page'] = 'Mes Favoris'
    context['results'] = products
    for element in context['results']:
        element['is_favourite'] = True
    return render(request, 'products/search.html', context=context)


def find_alternatives(request):
    ''' view getting alternatives to a product '''
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    category = product.category
    products = Product.objects.filter(
        category=category,
        nutriscore__lte=product.nutriscore).values()

    context = {}
    context['product_id']=product_id
    context['results'] = []
    for product in products:
        context['results'].append(product)

    # list all the user's favourite products
    users_favourite_products = []
    if request.user.is_authenticated:
        favourite_products = (Product.objects
                                .filter(in_users_favourites__id=request.user.id)
                                .values()
                                )
        for favourite_product in favourite_products:
            users_favourite_products.append(favourite_product)

    for product in context['results']:
        product['is_favourite'] = product in users_favourite_products
    context['page']= 'Find Alternatives'
    return render(request, 'products/search.html', context=context)
