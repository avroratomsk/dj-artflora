from home.models import BaseSettings 
 
def load_settings(request):
    return {'site_settings': BaseSettings.load()}

def setup(request):
    try:
        setup = BaseSettings.objects.get()
    except:
        setup = []
        
    return {"setup": setup}