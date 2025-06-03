from django.http import HttpResponse
from django.shortcuts import render, redirect

from home.models import BaseSettings, DeliveryPage, HomeTemplate, SliderHome, Stock
from cart.models import Cart
from home.forms import CallbackForm, ContactForm
from home.callback_send import email_callback
from favorites.models import Favorites
from shop.models import Category, Product
from reviews.models import Reviews
from django.http import JsonResponse

def callback(request):
  if request.method == "POST":
    form = CallbackForm(request.POST)
    if form.is_valid():
      name  = form.cleaned_data['name']
      phone = form.cleaned_data['phone']
      title = 'Заказ обратного звонка'
      messages = "Заказ обратного звонка:" + "\n" + "*ИМЯ*: " +str(name) + "\n" + "*ТЕЛЕФОН*: " + str(phone) + "\n"
      
      email_callback(messages, title)
      
      return JsonResponse({"success": "success"})
  else:
    return JsonResponse({'status': "error", 'errors': form.errors})
  
  return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def contact_email(request):
  if request.method == "POST":
    form = ContactForm(request.POST)
    if form.is_valid():
      name  = form.cleaned_data['name']
      phone = form.cleaned_data['phone']
      message = form.cleaned_data['message']
      title = 'Напишите нам'
      messages = "Заказ обратного звонка:" + "\n" + "*ИМЯ*: " +str(name) + "\n" + "*ТЕЛЕФОН*: " + str(phone) + "\n" + "*Сообщение*: " + str(message) + "\n"
      
      email_callback(messages, title)
      
      return JsonResponse({"success": "success"})
  else:
    return JsonResponse({'status': "error", 'errors': form.errors})
  
  return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def callback_success(request):
  return render(request, "pages/orders/callback-succes.html")

def privacy(request):
  return render(request, "pages/privacy.html")

def cookie(request):
  return render(request, "pages/cookie.html")

def index(request):
  products = Product.objects.filter(status=True)
  
  try: 
    home_page = HomeTemplate.objects.get()
    settings = BaseSettings.objects.get()
  except:
    home_page = HomeTemplate.objects.all()
    settings = BaseSettings.objects.all()

  category = Category.objects.all()[:8]
  
  saleProduct = Product.objects.filter(sale_price__gt=0)[:8]
  affordable_products = Product.objects.filter(price__gt=0, price__lt=2500)[:8]
  populate = Product.objects.filter(quantity_purchase__gte=10)[:8]
  novetly = Product.objects.filter(latest=True)[:8]
  reviews = Reviews.objects.filter(status=True)[:8]
  slider = SliderHome.objects.all()
  
  if request.user.is_authenticated:
    favorite_product_ids = Favorites.objects.filter(user=request.user).values_list('product_id', flat=True)
  else:
    favorite_product_ids = Favorites.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)
  
  # Добавляем флаг is_favorite к каждому продукту
  for product in products:
    product.is_favorite = product.id in favorite_product_ids
    
  # Добавляем флаг is_favorite к каждому продукту
  for product in populate:
    product.is_favorite = product.id in favorite_product_ids
    
  # Добавляем флаг is_favorite к каждому продукту
  for product in novetly:
    product.is_favorite = product.id in favorite_product_ids
  
  context = {
    "categorys": category,
    "populates": populate,
    "novetlys": novetly,
    "home_page": home_page,
    "products": saleProduct,
    "affordable": affordable_products,
    "settings": settings,
    "reviews": reviews,
    "slider": slider,
    "menus": products,
    # "form": form,
  }
  return render(request, 'pages/index.html', context)

def populate(request):
  products = Product.objects.filter(quantity_purchase__gte=10)
  
  if request.user.is_authenticated:
    favorite_product_ids = Favorites.objects.filter(user=request.user).values_list('product_id', flat=True)
  else:
    favorite_product_ids = Favorites.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)
  
  # Добавляем флаг is_favorite к каждому продукту
  for product in products:
    product.is_favorite = product.id in favorite_product_ids
  
  context = {
    "title": "Популярные товары",
    "products": products,
  }
  
  return render(request, "pages/populate.html", context)

def best_offer(request):
  free_shipping_products = Product.objects.filter(free_shipping=True)
  
  context = {
    "title": "Лучшие предложения",
    "free_shipping_products": free_shipping_products
  }
  
  return render(request, "pages/best_offer.html", context)

def stock_product(request):
  products = Product.objects.filter(discount__gte=1)
  
  context = {
    "title": "Товары по акции",
    "products": products
  }
  
  return render(request, "pages/stock-product.html", context)

def news(request):
  products = Product.objects.filter(latest=True)
  
  context = {
    "title": "Новинки",
    "products": products
  }
  
  return render(request, "pages/stock-product.html", context)

def about(request):
    category = Category.objects.all()[:12]
    context = {
      "categorys": category
    }
    return render(request, "pages/about.html", context)

def contact(request):
   
  form = ContactForm()
   
  context = {
    "form": form
  }
  
  return render(request, "pages/contact.html", context)

def stock(request):
    stocks = Stock.objects.filter(status=True)
    
    context = {
        "stocks": stocks
    }
    
    return render(request, "pages/stock/stock.html", context)

def stock_detail(request, slug):
    stock = Stock.objects.get(slug=slug)
    
    context = {
        "stock": stock
    }
    
    return render(request, "pages/stock/stock_detail.html", context)

def delivery(request):
  try:
    delivery_page = DeliveryPage.objects.get()
  except:
    delivery_page = None
    
  print(delivery_page)
    
  context = {
    "delivery_page":delivery_page
  }
  
  return render(request, "pages/delivery.html", context)

