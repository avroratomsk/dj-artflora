from home.models import BaseSettings 
from shop.models import Category
 
def load_settings(request):
    return {'site_settings': BaseSettings.load()}

def header_menu(request):
    return {"menu": Category.objects.filter(menu_add=True)}

def category(request):
    return {"categorys": Category.objects.all()}