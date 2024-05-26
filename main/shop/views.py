from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.db.models import Q
import itertools
from .services import *


from .models import *

def category(request):
  category = Category.objects.all()
  products = Product.objects.filter(status=True)
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
    
  products_all = Product.objects.filter(status=True)
  pr_char = ProductChar.objects.all()
  chars_all = ProductChar.objects.filter(parent__in=products_all)
  char_name = CharName.objects.filter(c_chars__in=chars_all, filter_add=True).exclude(filter_name=None).distinct()
  
  chars_list_name_noduble = []
  for li in chars_all:
    if li.char_value not in chars_list_name_noduble:
      chars_list_name_noduble.append(li.char_value)
  # print(chars_list_name_noduble)
  
  chars = ProductChar.objects.filter(char_value__in=chars_list_name_noduble).distinct()
  chars_list_name_noduble_a = ProductChar.objects.filter(parent__in=products_all).distinct().values_list('char_value', flat=True).distinct()
  
  context = {
    "pr_char":pr_char,
    "chars_all":chars_all,
    "products": products,
    "chars": chars,
    "char_name": char_name,
    "title": "Каталог",
    "parametrs_value": parametrs_value
  }

  return render(request, "pages/catalog/category.html", context)


def category_detail(request, slug):
  category = Category.objects.get(slug=slug)
  products = Product.objects.filter(category=category)
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
  
  chars = ProductChar.objects.filter(char_value__in=chars_list_name_noduble).distinct('char_value')
  
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
