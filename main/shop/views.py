from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.db.models import Q
import itertools

from favorites.models import Favorites
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
  if request.method == "GET":
    get_filtres = request.GET
    char_filtres_list = list(get_filtres.keys())
    parametrs_value = [request.GET.getlist(parametr) for parametr in char_filtres_list]
    merged_array = list(itertools.chain(*parametrs_value))
    product = ProductChar.objects.filter(char_value__in=merged_array)
    id_filter = [pr.parent.id for pr in product]
    
    if id_filter:
      products = products.filter(id__in=id_filter)

  char_name = chars()
  
  if request.user.is_authenticated:
    favorite_product_ids = Favorites.objects.filter(user=request.user).values_list('product_id', flat=True)
  else:
    favorite_product_ids = Favorites.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)
  
  for product in products:
    product.is_favorite = product.id in favorite_product_ids

  context = {
    "shop_settings": ShopSettings.objects.get(),
    "products": products,
    "chars": chars,
    "char_name": char_name,
    "title": "Каталог",
    "categorys": categorys
  }

  return render(request, "pages/catalog/category.html", context)


def category_detail(request, slug):
  category = Category.objects.get(slug=slug)
  products = Product.objects.filter(category=category).order_by('price')
  categories = Category.objects.all()
  
  if request.method == "GET":
    get_filtres = request.GET
      
    
    char_filtres_list = list(get_filtres.keys())
    parametrs_value = []
    for parametr in char_filtres_list:
      parametrs_value.append(request.GET.getlist(parametr))# [['Малиновый', 'Белый'], ['25']]
    
    merged_array = list(itertools.chain(*parametrs_value))
    product = ProductChar.objects.filter(char_value__in=merged_array)
    
    id_filter = [pr.parent.id for pr in product]
    
    if id_filter:
        products = products.filter(id__in=id_filter)
    
  char_name = chars()
  
  if request.user.is_authenticated:
    favorite_product_ids = Favorites.objects.filter(user=request.user).values_list('product_id', flat=True)
  else:
    favorite_product_ids = Favorites.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)
  
    
  # Добавляем флаг is_favorite к каждому продукту
  for product in products:
    product.is_favorite = product.id in favorite_product_ids
  
  
  context = {
    "category": category,
    "chars": chars,
    "char_name": char_name,
    "products": products,
    "categories": categories
  }
  
  return render(request, "pages/catalog/category-details.html", context)

def product(request, slug):
  product = Product.objects.get(slug=slug)
  products = Product.objects.all().exclude(slug=slug)[:4]
  context = {
    "title": "Название продукта",
    "product": product,
    "products":products
  }
  return render(request, "pages/catalog/product.html", context)


def search(request):
  query = request.GET.get('search', None)

  keywords = [word for word in query.split() if len(word) > 2]

  q_objects = Q()
  
  for token in keywords:
    q_objects |= Q(name__icontains=token)
    q_objects |= Q(category__name__icontains=token)
    q_objects |= Q(char_value__icontains=token)
  
  # char_product = ProductChar.objects.filter(char_value__icontains=query)
  
  products = Product.objects.filter(q_objects).order_by('price')
  
  # if request.method == "GET":
  #   get_filtres = request.GET
      
    
  #   char_filtres_list = list(get_filtres.keys())
  #   parametrs_value = []
  #   for parametr in char_filtres_list:
  #     parametrs_value.append(request.GET.getlist(parametr))# [['Малиновый', 'Белый'], ['25']]
    
  #   merged_array = list(itertools.chain(*parametrs_value))
  #   product = ProductChar.objects.filter(char_value__in=merged_array)
    
  #   id_filter = [pr.parent.id for pr in product]
    
  #   if id_filter:
  #       products = products.filter(id__in=id_filter)
    
  # products_all = Product.objects.filter(status=True)
  
  # id_product = []
  # for id in products_all:
  #   id_product.append(id.id)
    
  # chars_all = ProductChar.objects.filter(parent__in=products_all).distinct()
  # char_name = CharName.objects.filter(c_chars__in=chars_all, filter_add=True).exclude(filter_name=None).distinct()
  
  # chars_list_name_noduble = []
  # for li in chars_all:
  #   if li.char_value not in chars_list_name_noduble:
  #     chars_list_name_noduble.append(li.char_value)
  # # print(chars_list_name_noduble)
  
  # chars = ProductChar.objects.filter(char_value__in=chars_list_name_noduble).distinct()
  # chars_list_name_noduble_a = ProductChar.objects.filter(parent__in=products_all).distinct().values_list('char_value', flat=True).distinct()
  
  context = {
    # "char_name":char_name,
    # "chars": chars,
    "products": products,
    "category": "Страницы поиска",
    "title": "Страница поиска",
  }
  
  return render(request, "pages/catalog/category.html", context)
