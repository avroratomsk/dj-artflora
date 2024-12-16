from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.db.models import Q
import itertools

from favorites.models import Favorites
from admin.forms import ProductFilterForm
from .services import *
from .models import *
from django.db.models import F
      
from django.db.models import Count
from collections import defaultdict
def chars():
    unique_chars = []
    char_names = CharName.objects.prefetch_related('c_chars')
    for char_name in char_names:
        unique_values = set()
        unique_product_chars = (
            char_name.c_chars
            .values('id', 'char_value')
            .annotate(num_values=Count('char_value'))
            .filter(num_values=1)
        )
        for item in unique_product_chars:
          if item['char_value'] not in unique_values:
            unique_values.add(item['char_value'])
            unique_chars.append({
              'char': char_name.text_name,
              'id': item['id'],
              'char_value': item['char_value']
            })

    result_dict = defaultdict(list)
    for item in unique_chars:
        result_dict[item['char']].append((item['char_value'], item['id']))
    result_dict = dict(result_dict)
    return result_dict

def category(request):
    products = Product.objects.filter(status=True).order_by('price')
    categorys = Category.objects.all()

    try:
        shop_settings =  ShopSettings.objects.get()
    except:
        shop_settings = ShopSettings()


    filter_form = ProductFilterForm(request.GET)
    if filter_form.is_valid():
        q_objects = Q()
        for char_name in CharName.objects.filter(filter_add=True):
            value_ids = filter_form.cleaned_data.get(char_name.filter_name)
            if value_ids:
                q_objects |= Q(chars__char_name=char_name, chars__char_value__in=value_ids)
        
        if q_objects:
            products = products.filter(q_objects).distinct()

    # Избранные товары
    if request.user.is_authenticated:
        favorite_product_ids = Favorites.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        favorite_product_ids = Favorites.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)

    for product in products:
        product.is_favorite = product.id in favorite_product_ids

    context = {
        "shop_settings": shop_settings,
        "products": products,
        "filter_form": filter_form,
        "title": "Каталог",
        "categorys": categorys
    }

    return render(request, "pages/catalog/category.html", context)


def category_detail(request, slug):
  category = Category.objects.get(slug=slug)
  products = Product.objects.filter(category=category).order_by('price')
  categories = Category.objects.all()[:10]
  
  filter_form = ProductFilterForm(request.GET)
  if filter_form.is_valid():
      q_objects = Q()
      for char_name in CharName.objects.filter(filter_add=True):
          value_ids = filter_form.cleaned_data.get(char_name.filter_name)
          if value_ids:
              q_objects |= Q(chars__char_name=char_name, chars__char_value__in=value_ids)
      
      if q_objects:
          products = products.filter(q_objects).distinct()
  
  if request.user.is_authenticated:
    favorite_product_ids = Favorites.objects.filter(user=request.user).values_list('product_id', flat=True)
  else:
    favorite_product_ids = Favorites.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)
  
    
  # Добавляем флаг is_favorite к каждому продукту
  for product in products:
    product.is_favorite = product.id in favorite_product_ids
  
  
  context = {
    "category": category,
    "filter_form": filter_form,
    "products": products,
    "categories": categories
  }
  
  return render(request, "pages/catalog/category-details.html", context)

def product(request, slug):
  product = Product.objects.get(slug=slug)
  products = Product.objects.all().exclude(slug=slug)[:4]
  images = ProductImage.objects.filter(parent_id=product.id)[:3]

  context = {
    "title": "Название продукта",
    "product": product,
    "products":products,
    "images": images,
  }
  return render(request, "pages/catalog/product.html", context)


def search(request):
  query = request.GET.get('search', None)

  keywords = [word for word in query.split() if len(word) > 2]

  q_objects = Q()
  
  for token in keywords:
    q_objects |= Q(name__icontains=token)
    q_objects |= Q(category__name__icontains=token)
  
  products = Product.objects.filter(q_objects).order_by('price')
  
  
  context = {
    "products": products,
    "category": "Страницы поиска",
    "title": "Страница поиска",
  }
  
  return render(request, "pages/catalog/category.html", context)
