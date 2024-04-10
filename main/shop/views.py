from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.db.models import Q

from .services import *


from .models import *

def category(request):
  category = Category.objects.all()
  
  for cat in category:
    cat.product_count = cat.product_set.count() # Получаем количество товаров в каждой категории
  
  context = {
    "title": "Заголовок категорий",
    "categorys": category,
  }

  return render(request, "pages/catalog/category.html", context)


def category_detail(request, slug):
  category = Category.objects.get(slug=slug)
  products = Product.objects.filter(category=category)
  
  context = {
    "category_name": category.name,
    "title": "Название товара",
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
