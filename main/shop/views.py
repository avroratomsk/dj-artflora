from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.db.models import Q

from .services import *


from .models import *

def catalog(request):
  category = Categories.objects.all()
  
  context = {
    "title": "Заголовок категорий",
    "category": category,
  }

  return render(request, "pages/catalog/products.html", context)


def category_detail(request, slug=None):
  page = request.GET.get('page', 1)
  query = request.GET.get('q', None)
  category_name = get_object_or_404(Categories, slug=slug)
  category = Categories.objects.all()
  
  days = Day.objects.all()
  day_default = get_slug_day(datetime.today().isoweekday())
  day_filter = request.GET.get('day', day_default)
  
  if slug == "all":
    products =  Product.objects.all()
    
  # elif query:  
  #   products = q_search(query)
  else:
    products = Product.objects.filter(Q(category__slug=slug) & Q(day__slug=day_filter)) 
  paginator = Paginator(products, 3)
  current_page = paginator.page(int(page))
  
  context = {
    "title": f"{ category_name.name }",
    "products": current_page,
    "category": category,
    "day_names": days,
    "give_today": day_default
  }
  return render(request, "pages/catalog/single.html", context)

def product(request, slug):
  
  product = get_object_or_404(Product, slug=slug)
  # products = Product.objects.filter(~Q(slug=slug), category__pk=product.category.id)
  products = Product.objects.filter(category__pk=product.category.id).exclude(slug=slug)
  
  
  context = {
    "products": products,
    "product": product,
    "prod_slug": slug,
  }
  return render(request, "pages/catalog/view-product.html", context)
