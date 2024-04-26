from home.models import BaseSettings 
from shop.models import Category, Product
 
def load_settings(request):
    return {'site_settings': BaseSettings.load()}

def header_menu(request):
    return {"menu": Category.objects.filter(menu_add=True)}

def product_menu(request):
    return{"product_menu": Product.objects.all()}

def slider_category(request):
    return {"slider_category": Category.objects.filter(first_block_home=True)[:2]}

def category(request):
    return {"categorys": Category.objects.all()}