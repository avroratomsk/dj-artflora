from django.http import HttpResponse
from django.shortcuts import render

from home.models import BaseSettings, HomeTemplate, Stock
from shop.models import Product
from reviews.models import Reviews




def index(request):
    page = request.GET.get('page', 1)
    
    try:
        home_page = HomeTemplate.objects.get()
        settings = BaseSettings.objects.get()
    except:
        settings = BaseSettings.objects.all()
        home_page = HomeTemplate.objects.all()
        
    product = Product.objects.all()
    reviews = Reviews.objects.filter(status=True)
    
    context = {
        "home_page": home_page,
        "products": product,
        "settings": settings,
        "reviews": reviews,
    }
    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, "pages/about.html")

def contact(request):
    return render(request, "pages/contact.html")

def stock(request):
    stocks = Stock.objects.filter(status=True)
    
    context = {
        "stocks": stocks
    }
    
    return render(request, "pages/stock/stock.html", context)

def stock_detail(request, slug):
    stock = Stock.objects.get(slug=slug)
    
    context = {
        "stock": stock
    }
    
    return render(request, "pages/stock/stock_detail.html", context)
