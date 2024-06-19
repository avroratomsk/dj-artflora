from home.models import BaseSettings, Messanger 
from home.forms import CallbackForm
from favorites.models import Favorites
from reviews.models import Reviews
from shop.models import Category, Product
 
def load_settings(request):
    return {'site_settings': BaseSettings.load()}

def header_menu(request):
    return {"menu": Category.objects.filter(menu_add=True)[:6]}

def menus(request):
    return {"menus_pr": Product.objects.all()}

def callback(request):
    return {"callback_form": CallbackForm()}

def slider_category(request):
    return {"slider_category": Category.objects.filter(first_block_home=True)[:2]}

def category(request):
    return {"categorys": Category.objects.all()}

def reviews(request):
    return {"reviews": Reviews.objects.filter(status=True)}

def messanger_header(request):
    return {"messanger_header": Messanger.objects.filter(header_view=True)}

def messanger_footer(request):
    return {"messanger_footer": Messanger.objects.filter(footer_view=True)}

def favorites(request):
  if request.user.is_authenticated:
    favorites_count = Favorites.objects.filter(user=request.user).count()
  else:
    session_key = request.session.session_key
    
    if not session_key:
      request.session.create()
      session_key = request.session.session_key
    favorites_count = Favorites.objects.filter(session_key=session_key).count
    
  return {"favorites_count": favorites_count}
    