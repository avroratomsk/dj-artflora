from django.http import HttpResponse
from django.shortcuts import render

from home.models import BaseSettings, HomeTemplate, Stock
from shop.models import Product, Categories
from reviews.models import Reviews




def index(request):
    page = request.GET.get('page', 1)
    
    try:
        home_page = HomeTemplate.objects.get()
        settings = BaseSettings.objects.get()
    except:
        settings = BaseSettings.objects.all()
        home_page = HomeTemplate.objects.all()
        
    stock = Stock.objects.filter(status=True)
    link_category_main = Categories.objects.filter(add_banner=True).order_by("-id")[0:2]
    product = Product.objects.all()
    reviews = Reviews.objects.filter(status=True)
    
    context = {
        "stock": stock,
        "link_category_main": link_category_main,
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
