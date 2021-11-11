from django.shortcuts import render
from django.contrib import messages

from .models import Product, Category

def index(request):
    return render(request, 'products/index.html')

def search(request):
    req = request.GET['search']
    context={}
    context['search']=req
    
    products = Product.objects.filter(name__icontains=req).values()
    context['results'] = products

    return render(request, 'products/search.html', context=context)

def product(request):
    req = request.GET['id']
    context={}
    try:
        product = Product.objects.get(id=req)
    except:
        messages.add_message(request, messages.ERROR, "product not found")
        return render(request, 'products/index.html', status=404)
    context['product'] = {
        'name':product.name,
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
    }

      
    # déterminer si l'aliment est favori de l'utilisateur, pour ça:

        # l'utilisateur est connecté:
            # chercher si l'aliment est un favori de l'utilisateur
            # context['product']['is_favourite'] = True or False selon si favori ou non
            # context['user']['email'] = user.email -> ?
            # changement de style dans le template: couleur et value du bouton
        # l'utilisateur n'est pas connecté:
            # changement de style dans le template: couleur du bouton -> grisé + désactivé

    return render(request, 'products/product.html', context=context)
        

def toggle_favourite(request):
    return render(request,)