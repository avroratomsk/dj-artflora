from home.models import BaseSettings 
from shop.models import Categories
 
def load_settings(request):
    return {'site_settings': BaseSettings.load()}

def get_main_menu(request):
    return {'mainmenu': Categories.objects.filter(add_menu=True)}

def setup(request):
    try:
        setup = BaseSettings.objects.get()
    except:
        setup = []
        
    return {"setup": setup}