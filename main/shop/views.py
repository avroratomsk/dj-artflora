from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.db.models import Q
import itertools
from .services import *
from .models import *
from django.db.models import F
def category(request):
  products = Product.objects.filter(status=True).order_by('price')
  
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
    
  products_all = Product.objects.filter(status=True)
  
  id_product = []
  for id in products_all:
    id_product.append(id.id)
    
  chars_all = ProductChar.objects.filter(parent__in=products_all).distinct()
  char_name = CharName.objects.filter(c_chars__in=chars_all, filter_add=True).exclude(filter_name=None).distinct()
  
  chars_list_name_noduble = []
  for li in chars_all:
    if li.char_value not in chars_list_name_noduble:
      chars_list_name_noduble.append(li.char_value)
  # print(chars_list_name_noduble)
  
  chars = ProductChar.objects.filter(char_value__in=chars_list_name_noduble).distinct('char_value')
  
  # print(chars)
  # print('----------------')
  chars_list_name_noduble_a = ProductChar.objects.filter(parent__in=products_all).distinct().values_list('char_value', flat=True).distinct()
  context = {
    "products": products,
    "chars": chars,
    "char_name": char_name,
    "title": "Каталог",
  }

  return render(request, "pages/catalog/category.html", context)


def category_detail(request, slug):
  category = Category.objects.get(slug=slug)
  products = Product.objects.filter(category=category).order_by('price')
  groups = CharGroup.objects.all()
  
  
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
    
  products_all = Product.objects.filter(status=True, category_id=category)
  chars_all = ProductChar.objects.filter(parent__in=products_all).distinct()
  char_name = CharName.objects.filter(c_chars__in=chars_all, filter_add=True).exclude(filter_name=None).distinct()
  
  chars_list_name_noduble = []
  for li in chars_all:
    if li.char_value not in chars_list_name_noduble:
      chars_list_name_noduble.append(li.char_value)
  
  chars = ProductChar.objects.filter(char_value__in=chars_list_name_noduble).distinct()
  
  chars_list_name_noduble_a = ProductChar.objects.filter(parent__in=products_all).distinct().values_list('char_value', flat=True).distinct()
  
  
  context = {
    "category_name": category.name,
    "title": category.name,
    "chars": chars,
    "char_name": char_name,
    "products": products
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
