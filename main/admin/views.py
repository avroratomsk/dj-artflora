import subprocess
import xlrd

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from admin.forms import CategoryForm, DayForm, FillialForm, GlobalSettingsForm, HomeTemplateForm, ProductForm, ReviewsForm, ServiceForm, StockForm
from home.models import BaseSettings, HomeTemplate, Stock
from service.models import Service
from reviews.models import Reviews
from shop.models import Product,Categories,Day,Subsidiary
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
# from django.contrib.auth.decorators import user_passes_test

# @user_passes_test(lambda u: u.is_superuser)
# def sidebar_show(request): 
   
#     request.session['sidebar'] = 'True' 
    
#     return redirect('admin')

# @user_passes_test(lambda u: u.is_superuser)

def admin(request):
  """Данная предстовление отобразает главную страницу админ панели"""
  return render(request, "page/index.html")

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
      
      print("Все хорошо")
      # subprocess.call(["touch", RESET_FILE])
      return redirect("admin")
    else:
      return render(request, "settings/general_settings.html", {"form": form_new})

  settings = BaseSettings.objects.get()

  form = GlobalSettingsForm(instance=settings)
  context = {
    "form": form,
    "settings":settings
  }  

  return render(request, "settings/general_settings.html", context)

def admin_product(request):
  """
  View, которая возвращаяет и отрисовывает все товары на странице
  и разбивает их на пагинацию 
  """
  page = request.GET.get('page', 1)
  
  products = Product.objects.all()
  paginator = Paginator(products, 10)
  current_page = paginator.page(int(page))
  
  context = {
    "products": current_page
  }
  return render(request, "shop/product/product.html", context)

def product_edit(request, pk):
  """
    View, которая получает данные из формы редактирования товара
    и изменяет данные внесенные данные товара в базе данных
  """
  product = Product.objects.get(id=pk)
  form = ProductForm(instance=product)
  
  form_new = ProductForm(request.POST, request.FILES, instance=product) 
  if request.method == 'POST':
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_product')
    else:
      return render(request, 'shop/product/product_edit.html', {'form': form_new,})
  context = {
    "form":form
  }
  return render(request, "shop/product/product_edit.html", context)

def product_add(request):
  form = ProductForm()
  
  if request.method == "POST":
    form_new = ProductForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_product')
    else:
      return render(request, "shop/product/product_add.html", {"form": form_new})
    
  context = {
    "form": form
  }
  
  return render(request, 'shop/product/product_add.html', context)

def product_delete(request,pk):
  product = Product.objects.get(id=pk)
  product.delete()
  
  return redirect('admin_product')

class UploadingProducts(object):
  # prod = Product.objects.all()
  # prod.delete()
  
  foreign_key_fields = ["category","day"]
  model = Product
  
  
  def __init__(self, data):
    data = data
    self.uploaded_file = data.get("file")
    self.parsing()
    
  def getting_related_model(self, field_name):
    related_model = self.model._meta.get_field(field_name).remote_field.model
    return related_model
  
  def getting_headers(self):
    s = self.s 
    headers = dict()
    for column in range(s.ncols):
      value = s.cell(0, column).value
      headers[column] = value
    return headers
  
  def parsing(self):
    uploaded_file = self.uploaded_file
    wb = xlrd.open_workbook(file_contents=uploaded_file.read())
    s = wb.sheet_by_index(0)
    self.s = s
    
    headers = self.getting_headers()
    print(f"{headers} -  Заголовки")
    
    product_bulk_list = list()
    for row in range(1, s.nrows):
      row_dict = {}
      for column in range(s.ncols):
        value = s.cell(row,column).value
        field_name = headers[column]
        
        if field_name == "id" and not value:
          continue
        
        if field_name == "date" and not value:
          continue
        
        if field_name in self.foreign_key_fields:
          related_model = self.getting_related_model(field_name)
          print(related_model)
          
          isinstance, created = related_model.objects.get_or_create(name=value)
          value = isinstance
        row_dict[field_name] = value
      
      print(row_dict)
      # product_bulk_list.append(Product(**row_dict))
      Product.objects.create(**row_dict)
    
    # Product.objects.bulk_create(product_bulk_list)
    # return True

def upload_goods(request):
  if request.POST:
    print(request.POST)
    print(request.FILES)
    file = request.FILES['upload_file']
    uploading_file = UploadingProducts({"file": file})
    if uploading_file:
      print('Успешная загрузка')
    else:
      print('Ошибка загрузки файла')
  else:
    print("Не метод POST")
      
  return render(request, "upload/upload.html")

def admin_category(request):
  categorys = Categories.objects.all()
  
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
  categorys = Categories.objects.get(id=pk)
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
  category = Categories.objects.get(id=pk)
  category.delete()
  
  return redirect('admin_category')

def day_product(request):
  days = Day.objects.all().exclude(slug="ezhednevno")
  
  context = {
    "days": days,
  }
  
  return render(request, "days/days.html", context)

def day_edit(request, pk):
  day = Day.objects.get(id=pk)
  form = DayForm(instance=day)
  
  form_new = DayForm(request.POST, instance=day)
  if request.method == "POST":
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_day")
    else:
      return render(request, "days/days_edit.html", {"form": form_new})

  context = {
    "form": form,
  }
  
  return render(request, "days/days_edit.html", context)

def day_add(request):
  form = DayForm()
  if request.method == "POST":
    form_new = DayForm(request.POST)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_day")
    else:
      return render(request, "days/days_add.html", {"form": form_new})
  context = {
    "form": form
  }
  
  return render(request, "days/days_add.html", context)

def admin_fillial(request):
  fillials = Subsidiary.objects.all()
  
  context = {
    "fillials": fillials
  }
  
  return render(request, "fillials/fillial.html", context)

def fillial_edit(request, pk):
  fillial = Subsidiary.objects.get(id=pk)
  form = FillialForm(instance=fillial)
  
  if request.method == "POST":
    form_new = FillialForm(request.POST, request.FILES, instance=fillial)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_fillial")
    else:
      return render(request, "fillials/fillial_edit.html", {"form": form_new})
  
  context = {
    "form": form,
  }
  
  return render(request, "fillials/fillial_edit.html", context)

def fillial_add(request):
  form = FillialForm()
  if request.method == "POST":
    form_new = FillialForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_fillial")
    else:
      return render(request, "fillials/fillial_add.html", {"form": form_new})
    
  context = {
    "form": form
  }
  
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
      
      print("Все хорошо")
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
    "reviews": reviews
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

def admin_stock(request):
  stocks = Stock.objects.all()
  
  context = {
    "stocks": stocks
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