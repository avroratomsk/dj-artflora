import math
import os
import zipfile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from admin.forms import *
from home.models import BaseSettings, DeliveryPage, HomeTemplate, Messanger, SliderHome, Stock
from coupons.models import Coupon
from order.models import Order, OrderItem
from main.settings import BASE_DIR
from users.models import User
from service.models import Service
from reviews.models import Reviews
from shop.models import CharGroup, CharName, Product,Category, ProductChar, ProductImage, ShopSettings
from django.core.paginator import Paginator
from django.core.files.images import ImageFile
from django.shortcuts import render, get_object_or_404, get_list_or_404
import openpyxl
import pandas as pd
from django.contrib.auth.decorators import user_passes_test

# @user_passes_test(lambda u: u.is_superuser)
# def sidebar_show(request): 
   
#     request.session['sidebar'] = 'True' 
    
#     return redirect('admin')


@user_passes_test(lambda u: u.is_superuser)
def admin(request):
  no_register = OrderItem.objects.all()
  
  """Данная предстовление отобразает главную страницу админ панели"""
  
  context = {
    "no_register": no_register
  }
  return render(request, "page/index.html", context)

def admin_settings(request):
  try:
    settings = BaseSettings.objects.get()
  except:
    settings = BaseSettings()
    settings.save()
    
  if request.method == "POST":
    form_new = GlobalSettingsForm(request.POST, request.FILES, instance=settings)
    if form_new.is_valid():
      form_new.save()
      # subprocess.call(["touch", RESET_FILE])
      return redirect("admin")
    else:
      return render(request, "settings/general_settings.html", {"form": form_new})

  settings = BaseSettings.objects.get()

  form = GlobalSettingsForm(instance=settings)
  
  context = {
    "form": form,
    "settings":settings,
  }  

  return render(request, "settings/general_settings.html", context)

def admin_messanger(request):
  messanger = Messanger.objects.all().order_by('name')
  
  context = {
    "messangers": messanger
  }
  return render(request, "settings/messanger.html", context)

def messanger_add(request):
  form = MessangerForm()
  
  if request.method == "POST":
    form_new = MessangerForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect('messanger')
    else:
      return render(request, "settings/messanger_add.html", {"form": form_new})
    
  context = {
    "form": form,
  }
  
  return render(request, "settings/messanger_add.html", context)

def messanger_edit(request, pk):
  messanger = Messanger.objects.get(id=pk)
  form = MessangerForm(instance=messanger)
  
  form_new = MessangerForm(request.POST, request.FILES, instance=messanger)
  if request.method == "POST":
    if form_new.is_valid():
      form_new.save()
      return redirect('messanger')
    else:
      return render(request, "settings/messanger_edit.html", {"form": form_new})
    
  context = {
    "form": form,
  }
  
  return render(request, "settings/messanger_edit.html", context)

def messanger_delete(request, pk):
  messanger = Messanger.objects.get(id=pk)
  messanger.delete()
  return redirect('messanger')

def admin_shop(request):
  try:
    shop_setup = ShopSettings.objects.get()
    form = ShopSettingsForm(instance=shop_setup)
  except:
    form = ShopSettingsForm()
    
  if request.method == "POST":
    try:
      shop_setup = ShopSettings.objects.get() 
    except:
      shop_setup = None
    
    form_new = ShopSettingsForm(request.POST, request.FILES, instance=shop_setup)
    if form_new.is_valid:
      form_new.save()
      
      return redirect('admin_shop')
    else:
      return render(request, "shop/settings.html", {"form": form})
  
  context = {
    "form": form,
  }
  return render(request, "shop/settings.html", context)

def admin_product(request):
  """
  View, которая возвращаяет и отрисовывает все товары на странице
  и разбивает их на пагинацию 
  """
  page = request.GET.get('page', 1)
  
  products = Product.objects.all()
  paginator = Paginator(products, 15)
  current_page = paginator.page(int(page))
  
  context = {
    "items": current_page
  }
  return render(request, "shop/product/product.html", context)

def orders(request):
    items = Order.objects.prefetch_related('items').all().order_by('-id')

    context = {
        "items": items,
    }

    return render(request, "page/statistics.html", context)

def order_detail(request, pk):
  item = Order.objects.prefetch_related('items').get(id=pk)

  context = {
      "item": item,
  }

  return render(request, "page/statistics_detail.html", context)

def order_delete(request, pk):
  item = Order.objects.get(id=pk)
  item.delete()

  return redirect(request.META.get("HTTP_REFERER", 'admin'))

def product_edit(request, pk):
    """
    View для редактирования товара + связанных изображений и характеристик
    """
    product = get_object_or_404(Product, id=pk)

    chars = ProductChar.objects.filter(parent_id=pk)
    all_chars = CharName.objects.all()
    images = ProductImage.objects.filter(parent_id=pk)


    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        #formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        product_char_form = ProductCharForm(request.POST)

        if form.is_valid():
            product = form.save()

            images = request.FILES.getlist('src')
            for image in images:
                img = ProductImage(parent=product, src=image)
                img.save()

            char_name = request.POST.getlist("text_name")
            char_value = request.POST.getlist("char_value")
            for name_id, value in zip(char_name, char_value):
                ProductChar.objects.create(
                    char_name_id=name_id,
                    parent=product,
                    char_value=value,
                )

            # 🔹 обновление старых характеристик
            old_char_id = request.POST.getlist("old_char_id")
            old_char_name = request.POST.getlist("old_text_name")
            old_char_value = request.POST.getlist("old_char_value")
            for cid, cname, cval in zip(old_char_id, old_char_name, old_char_value):
                old_char = ProductChar.objects.get(id=cid)
                old_char.char_name_id = cname
                old_char.char_value = cval
                old_char.save()

            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return render(
                request,
                "shop/product/product_edit.html",
                {
                    "form": form,
                    "formset": formset,
                    "product_char_form": product_char_form,
                    "all_chars": all_chars,
                    "chars": chars,
                },
            )

    else:
        form = ProductForm(instance=product)
        #formset = ProductImageFormSet(instance=product)
        product_char_form = ProductCharForm()

    return render(
        request,
        "shop/product/product_edit.html",
        {
            "form": form,
            #"formset": formset,
            "product_char_form": product_char_form,
            "all_chars": all_chars,
            "chars": chars,
            'images': images,
        },
    )
def product_image_delete(request, pk):
  image = get_object_or_404(ProductImage, pk=pk)
  product_id = image.parent.id
  image.delete()
  return redirect("product_edit", pk=product_id)

def product_add(request):
  form = ProductForm()
  product_char_form = ProductCharForm()
  image_form = ProductImageForm()
  if request.method == "POST":
    form_new = ProductForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      product = Product.objects.get(slug=request.POST['slug'])

      images = request.FILES.getlist('src')

      for image in images:
          img = ProductImage(parent=product, src=image)
          img.save()

      char_name = request.POST.getlist('text_name')
      char_value = request.POST.getlist('char_value')
      char_count = 0

      for char in char_name:

          value = char_value[char_count]
          product_char = ProductChar(
              char_name_id = char,
              parent = product,
              char_value = value
          )
          product_char.save()
          char_count += 1


      product.save()
      return redirect('admin_product')
    else:
      messages = "Форма не валидна"
      return render(request, "shop/product/product_add.html", {"form": form_new, "messages": messages})
    
  context = {
    "form": form,
    "product_char_form":product_char_form,
    'image_form': image_form,
  }
  
  return render(request, 'shop/product/product_add.html', context)

def product_delete(request,pk):
  product = Product.objects.get(id=pk)
  product.delete()
  
  return redirect('admin_product')

def admin_char(request):
  chars = CharName.objects.filter(group=None)
  groups = CharGroup.objects.all()
  
  context = {
        "groups": groups,
        "chars": chars
    }
  return render(request, "shop/char/char.html", context)

def char_add(request):
  if request.method == 'POST':
        form_new = CharNameForm(request.POST)
        if form_new.is_valid():
            form_new.save()
            return redirect('admin_char')
        else:
            return render(request, 'shop/char/char_add.html', {'form': form})

  form = CharNameForm()
  context = {
      'form': form,
  }
  return render(request, 'shop/char/char_add.html', context)

def char_edit(request, pk):
  char = CharName.objects.get(id=pk)
  
  if request.method == 'POST':
      form_new = CharNameForm(request.POST, instance=char)
      if form_new.is_valid():
          form_new.save()
          return redirect('admin_char')
      else:
          return render(request, 'shop/char/char_edit.html', {'form': form})

  form = CharNameForm(instance=char)
  context = {
      'form': form,
  }
  return render(request, 'shop/char/char_edit.html', context)

def char_delete(request, pk):
  char = CharName.objects.get(id=pk)
  char.delete()
  return redirect('admin_char')

def char_group_add(request):
  if request.method == 'POST':
      form_new = CharGroupForm(request.POST)
      if form_new.is_valid():
          form_new.save()
          return redirect('admin_char')
      else:
          return render(request, 'shop/char/char_group_add.html', {'form': form})

  form = CharGroupForm()
  context = {
      'form': form,
  }
  return render(request, 'shop/char/char_group_add.html', context)

def char_group_edit(request, pk):
  char_group = CharGroup.objects.get(id=pk)
  if request.method == "POST":
    form_new = CharGroupForm(request.POST, instance=char_group)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_char")
    else:
      return render(request, "shop/char/char_group_edit.html", {"form": form})
  form = CharGroupForm(instance=char_group)
  
  context = {
    "form": form,
  }
  
  return render(request, "shop/char/char_group_edit.html", context)


def char_group_delete(request, pk):
  char_group = CharGroup.objects.get(id=pk)
  char_group.delete()
  return redirect('admin_char')


folder = 'upload/'

from PIL import Image

def upload_goods(request):
    form = UploadFileForm()
    if request.method == 'POST':
      form = UploadFileForm(request.POST, request.FILES)
      if form.is_valid():
          file = request.FILES['file']
          destination = open(os.path.join('upload/', file.name), 'wb+')
          for chunk in file.chunks():
              destination.write(chunk)
          destination.close()
              
          # Распаковка архива
          with zipfile.ZipFile('upload/upload.zip', 'r') as zip_ref:
              zip_ref.extractall('media/')
              
          # Удаление загруженного архива
          os.remove('upload/upload.zip')
          
          # Сжатие фотографий
          for filename in os.listdir('media/upload'):
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.JPG') or filename.endswith('.JPEG'):
              with Image.open(os.path.join('media/upload', filename)) as img:
                img.save(os.path.join('media/goods', filename), quality=60)  # quality=60 для JPEG файла
                
          # Очистка временной папки
          os.system('rm -rf media/upload')
          return redirect('upload-succes')
      else:
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'form': form})

def upload_succes(request):
  return render(request, "upload/upload-succes.html")


path = f"{BASE_DIR}/upload/upload.xlsx"

from pytils.translit import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

def parse_exсel(path):
  workbook = openpyxl.load_workbook(path)
  sheet = workbook.active
  start_row = 2
    
  Product.objects.all().delete()

  for row in sheet.iter_rows(min_row=start_row, values_only=True):
    name = row[1]
    slug = slugify(name)
    description = row[3]
    meta_h1 = ''
    meta_title = ''
    meta_description = ''
    meta_keywords = ''
    try:
      image = f"goods/{row[4].split(';')[0]}"
      image_list = row[4].split(';')
    except:
      pass
    price = row[5]
    sale_price = 0.0
    
    if row[6] == None:
      discount = 0
    else:
      discount = int(row[6])
      sale_price = round(price - price * discount / 100, 1)
    quantity = row[8]
    if row[7]:
      category_name = row[7]
    else:
      pass
    category_slug = slugify(category_name)

    try:
      category = Category.objects.get(slug=category_slug)
    except ObjectDoesNotExist:
      if not Category.objects.filter(name=category_name).exists():
        category = Category.objects.create(
          name=category_name,
          slug=category_slug
        )
      else:
        category = Category.objects.filter(name=category_name).first()
    
    composition = row[9]
    diameter = row[10]
    height = row[11]
    quantity_flower = row[12]
    latest = False
    status = True
  
    try:
      new_product = Product.objects.get(slug=slug)
    except ObjectDoesNotExist:
      if not Product.objects.filter(name=name).exists():
        try:
            new_product = Product.objects.create(
            name=name,
            slug=slug,
            description=description,
            meta_h1=meta_h1,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            image=image,
            price=price,
            sale_price=sale_price,
            discount=discount,
            quantity=quantity,
            category=category,
            composition=composition,
            diameter=diameter,
            height=height,
            quantity_flower=quantity_flower,
            latest=latest,
            status=status
          )
        except Exception as e:
          pass
      else:
        new_product = Product.objects.filter(name=name).first() 
        
      for image in image_list:
        
        try:
          image_file = open('media/goods/' + image, 'rb')
          image_image = ImageFile(image_file)
          image_create = ProductImage.objects.create(
              parent=new_product,
              src=image_image
          )
        except Exception as e: 
          print(e)
# parse_exсel(path)

def admin_category(request):
  categorys = Category.objects.all().order_by('-id')
  
  context ={
    "categorys": categorys,
  }
  return render(request, "shop/category/category.html", context)

def category_add(request):
  form = CategoryForm()
  if request.method == "POST":
    form_new = CategoryForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_category")
    else:
      return render(request, "shop/category/category_add.html", {"form": form_new})
    
  context = {
    "form": form
  }
  return render(request, "shop/category/category_add.html", context)

def category_edit(request, pk):
  categorys = Category.objects.get(id=pk)
  if request.method == "POST":
    form = CategoryForm(request.POST, request.FILES, instance=categorys)
    if form.is_valid():
      form.save()
      return redirect("admin_category")
    else:
      return render(request, "shop/category/category_edit.html", {"form": form})
  
  context = {
    "form": CategoryForm(instance=categorys),
    "categorys": categorys
  }

  return render(request, "shop/category/category_edit.html", context)

def category_delete(request, pk):
  category = Category.objects.get(id=pk)
  category.delete()
  
  return redirect('admin_category')

def admin_slider(request):
  slider = SliderHome.objects.all()
  
  context ={
    "items": slider,
  }
  return render(request, "static/slider-home/slider.html", context)

def slider_add(request):
  form = SliderForm()
  if request.method == "POST":
    form_new = SliderForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_slider")
    else:
      return render(request, "static/slider-home/slider_add.html", {"form": form_new})
    
  context = {
    "form": form
  }
  return render(request, "static/slider-home/slider_add.html", context)

def slider_edit(request, pk):
  slide = SliderHome.objects.get(id=pk)
  if request.method == "POST":
    form = SliderForm(request.POST, request.FILES, instance=slide)
    if form.is_valid():
      form.save()
      return redirect("admin_slider")
    else:
      return render(request, "static/slider-home/slider_edit.html", {"form": form})
  form = SliderForm(instance=slide)
  context = {
    "form": form
  }
  return render(request, "static/slider-home/slider_edit.html", context)

def slider_delete(request, pk):
  slide = SliderHome.objects.get(id=pk)
  slide.delete()
  return redirect('admin_slider')

def day_product(request):
  pass
  # days = Day.objects.all().exclude(slug="ezhednevno")
  
  # context = {
  #   "days": days,
  # }
  
  # return render(request, "days/days.html", context)

def day_edit(request, pk):
  pass
  # day = Day.objects.get(id=pk)
  # form = DayForm(instance=day)
  
  # form_new = DayForm(request.POST, instance=day)
  # if request.method == "POST":
  #   if form_new.is_valid():
  #     form_new.save()
  #     return redirect("admin_day")
  #   else:
  #     return render(request, "days/days_edit.html", {"form": form_new})

  # context = {
  #   "form": form,
  # }
  
  # return render(request, "days/days_edit.html", context)

def day_add(request):
  pass
  # form = DayForm()
  # if request.method == "POST":
  #   form_new = DayForm(request.POST)
  #   if form_new.is_valid():
  #     form_new.save()
  #     return redirect("admin_day")
  #   else:
  #     return render(request, "days/days_add.html", {"form": form_new})
  # context = {
  #   "form": form
  # }
  
  # return render(request, "days/days_add.html", context)

def admin_fillial(request):
  pass
  # fillials = Subsidiary.objects.all()
  
  # context = {
  #   "fillials": fillials
  # }
  
  # return render(request, "fillials/fillial.html", context)

def fillial_edit(request, pk):
  pass
  # fillial = Subsidiary.objects.get(id=pk)
  # form = FillialForm(instance=fillial)
  
  # if request.method == "POST":
  #   form_new = FillialForm(request.POST, request.FILES, instance=fillial)
  #   if form_new.is_valid():
  #     form_new.save()
  #     return redirect("admin_fillial")
  #   else:
  #     return render(request, "fillials/fillial_edit.html", {"form": form_new})
  
  # context = {
  #   "form": form,
  # }
  
  # return render(request, "fillials/fillial_edit.html", context)

def fillial_add(request):
  pass
  # form = FillialForm()
  # if request.method == "POST":
  #   form_new = FillialForm(request.POST, request.FILES)
  #   if form_new.is_valid():
  #     form_new.save()
  #     return redirect("admin_fillial")
  #   else:
  #     return render(request, "fillials/fillial_add.html", {"form": form_new})
    
  # context = {
  #   "form": form
  # }
  
  return render(request, "fillials/fillial_add.html", context)

def admin_home(request):
  try:
    home_page = HomeTemplate.objects.get()
  except:
    home_page = HomeTemplate()
    home_page.save()
    
  if request.method == "POST":
    form_new = HomeTemplateForm(request.POST, request.FILES, instance=home_page)
    if form_new.is_valid():
      form_new.save()
      
      # subprocess.call(["touch", RESET_FILE])
      return redirect("admin")
    else:
      return render(request, "static/home_page.html", {"form": form_new})
  
  home_page = HomeTemplate.objects.get()
  
  form = HomeTemplateForm(instance=home_page)
  context = {
    "form": form,
    "home_page":home_page
  }  
  
  return render(request, "static/home_page.html", context)

def admin_reviews(request):
  reviews = Reviews.objects.all()
  
  context = {
    "items": reviews
  }
  
  return render(request, "reviews/reviews.html", context)

def admin_reviews_edit(request, pk):
  review = Reviews.objects.get(id=pk)
  form = ReviewsForm(instance=review)
  
  if request.method == "POST":
    form_new = ReviewsForm(request.POST, request.FILES, instance=review)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_reviews")
    else:
      return render(request, "reviews/reviews_edit.html", {"form": form_new})
  
  context = {
    "review":review,
    "form": form
  }
  
  return render(request, "reviews/reviews_edit.html", context)

def admin_reviews_add(request):
  form = ReviewsForm()
  if request.method == "POST":
    form_new = ReviewsForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_reviews")
    else:
      return render(request, "reviews/reviews_add.html", {"form": form_new})
    
  context = {
    "form": form
  }
  
  return render(request, "reviews/reviews_add.html", context)

def admin_reviews_delete(request, pk):
  review = Reviews.objects.get(id=pk)
  review.delete()
  return redirect("admin_reviews")

def admin_stock(request):
  stocks = Stock.objects.all()
  
  context = {
    "items": stocks
  }
  
  return render(request, "stock/stock.html", context)

def stock_add(request):
  form = StockForm()
  
  if request.method == "POST":
    form_new = StockForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_stock")
    else: 
      return render(request, "stock/stock_add.html", {"form": form_new})
  
  context = {
    "form": form
  }
  
  return render(request, "stock/stock_add.html", context)

def stock_edit(request, pk):
  stock = Stock.objects.get(id=pk)
  form = StockForm(instance=stock)
  if request.method == "POST":
    form_new = StockForm(request.POST, request.FILES, instance=stock)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_stock")
    else:
      return render(request, "stock/stock_edit.html", {"form": form_new})
  
  context = {
    "form": form
  }
  
  return render(request, "stock/stock_edit.html", context)

def stock_delete(request, pk):
  stock = Stock.objects.get(id=pk)
  stock.delete()
  return redirect("admin_stock")

def admin_service(request):
  services = Service.objects.all()
  
  context = {
    "services": services
  }
  
  return render(request, "serv/admin_serv.html", context)

def service_add(request):
  form = ServiceForm()
  
  if request.method == "POST":
    form_new = ServiceForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_service")
    else: 
      return render(request, "serv/serv_add.html", {"form": form_new})
  
  context = {
    "form": form
  }
  
  return render(request, "serv/serv_add.html", context)

def service_edit(request, pk):
  services = Service.objects.get(id=pk)
  form = ServiceForm(instance=services)
  if request.method == "POST":
    form_new = ServiceForm(request.POST, request.FILES, instance=services)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_service")
    else:
      return render(request, "serv/stock_edit.html", {"form": form_new})
  
  context = {
    "form": form
  }
  
  return render(request, "serv/serv_edit.html", context)

def service_delete(request, pk):
  service = Service.objects.get(id=pk)
  service.delete()
  return redirect("admin_service")


# !!! МАРКЕТИНГ !!!
# Промокоды

def admin_promo(request):
    coupons = Coupon.objects.all()
    context = {
        'items': coupons
    }

    return render(request, 'marketing/promo.html', context)


def promo_add(request):
  if request.method == 'POST':
    form = CouponForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('admin_promo')
    else:
      return render(request, 'marketing/promo_add.html', {'form':form})

  form = CouponForm()
  context = {
      'form': form
  }

  return render(request, 'marketing/promo_add.html', context)

def promo_edit(request, pk):
  coupon = Coupon.objects.get(id=pk)

  if request.method == 'POST':
    form = CouponForm(request.POST, instance=coupon)
    if form.is_valid():
      form.save()
      return redirect('admin_promo')
    else:
      return render(request, 'marketing/promo_edit.html', {'form':form})
  form = CouponForm(instance=coupon)
  context = {
    'form': form,
    'coupon': coupon,
  }

  return render(request, 'marketing/promo_edit.html', context)


def promo_delete(request, pk):
    coupon = Coupon.objects.get(id=pk)
    coupon.delete()
    return redirect('admin_promo')
  
def admin_delivery(request):
  # Попытка получить существующую запись, если нет - создать новую
  delivery_page, created = DeliveryPage.objects.get_or_create(pk=1)
  
  if request.method == "POST":
    form = DeliveryPageForm(request.POST, request.FILES, instance=delivery_page)
    if form.is_valid():
      form.save()
      return redirect(request.META.get("HTTP_REFERER", 'admin'))
  else:
    form = DeliveryPageForm(instance=delivery_page)

  context = {
    "form": form,
    "delivery_page": delivery_page
  }  
  
  return render(request, "static/delivery_page.html", context)


def admin_users(request):
  users = User.objects.all()
  
  return render(request, "users/admin_users.html", {"items": users})


def admin_contact(request):
  pass
  
