from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from favorites.models import Favorites
from shop.models import Product
import json

def favorites(request):
  favorites = Favorites.objects.all()
  
  context = {
    "favorites": favorites
  }
  return render(request, "pages/favorites/favorites.html", context)


def favorites_toggle(request):
  # data = json.loads(request.body)
  # idProduct = data.get('dataId')
  # product = get_object_or_404(Product, id=idProduct)
  
  # if request.user.is_authenticated:
  #   user = request.user
  # else:
  #   user=None
  #   session_key = request.session.session_key
  
  # favorites, created = Favorites.objects.get_or_create(user=user, session_key=session_key, product=product)
  
  # if not created:
  #   favorites.delete()
  #   return JsonResponse({"status": "removed"}) 
  
  return JsonResponse({"status": "added"})


def favorites_check(request):
  
  if request.user.is_authenticated:
    user = request.user
  else:
    user=None
    session_key = request.session.session_key
    
  favorites_count = Favorites.objects.filter(user=user, session_key=session_key).count()
  return JsonResponse({"count": favorites_count})
