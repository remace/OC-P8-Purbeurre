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
        'off_link': product.off_link,
        'nutriscore': product.nutriscore,
    }
    return render(request, 'products/product.html', context=context)
        

def toggle_favourite(request):
    pass