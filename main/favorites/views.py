from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from favorites.models import Favorites
from shop.models import Product
import json

def favorites(request):
  favorites = Favorites.objects.all()
  
  if request.user.is_authenticated:
    favorite_product_ids = Favorites.objects.filter(user=request.user).values_list('product_id', flat=True)
  else:
    favorite_product_ids = Favorites.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)
  
    
  # Добавляем флаг is_favorite к каждому продукту
  for product in favorites:
    product.is_favorite = product.id in favorite_product_ids
  
  context = {
    "favorites": favorites
  }
  return render(request, "pages/favorites/favorites.html", context)


def favorites_toggle(request):
  data = json.loads(request.body)
  idProduct = data.get('dataId')
  product = get_object_or_404(Product, id=idProduct)
  
  if request.user.is_authenticated:
    user = request.user
    session_key = request.session.session_key
  else:
    user=None
    session_key = request.session.session_key
  
  favorites, created = Favorites.objects.get_or_create(user=user, session_key=session_key, product=product)
  
  if not created:
    favorites.delete()
    return JsonResponse({"status": "removed", "name": favorites.product.name }) 
  
  return JsonResponse({"status": "added", "name": favorites.product.name })


def favorites_check(request):
  
  if request.user.is_authenticated:
    user = request.user
    session_key = request.session.session_key
  else:
    user=None
    session_key = request.session.session_key
    
  favorites_count = Favorites.objects.filter(user=user, session_key=session_key).count()
  return JsonResponse({"count": favorites_count})
