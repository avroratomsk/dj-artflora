from datetime import datetime
from django.shortcuts import get_list_or_404
from django.db.models import Q

# from shop.models import Product, Day

def get_name_day():
  today = datetime.today()
  year = today.year 
  month = today.month 
  day = today.day
  
  date  = f'{today.year}-{today.month}-{today.day}'
  day_id = today.weekday()
  
  if(day_id == 1):
    day_slug = "Понедельник"
    
  if(day_id == 1):
    day_slug = "Вторник"
    
  if(day_id == 2):
    day_slug = "Среда"
    
  if(day_id == 3):
    day_slug = "Четверг"
  
  if(day_id == 4):
    day_slug = "Пятница"
    
  if(day_id == 5):
    day_slug = "Суббота"
    
  if(day_id == 6):
    day_slug = "Воскресенье"
  
  return day_slug


def get_slug_day(day_id):
  
  if(day_id == 1):
    day_slug = "mon"
    
  if(day_id == 2):
    day_slug = "tue"
    
  if(day_id == 3):
    day_slug = "wed"
    
  if(day_id == 4):
    day_slug = "thu"
  
  if(day_id == 5):
    day_slug = "fri"
    
  if(day_id == 6):
    day_slug = "sat"
    
  if(day_id == 7):
    day_slug = "sun"
  
  return day_slug

# get_slug_day(4)
  


def q_search(query):
  """
    Данная функция реализовывает поиск:
      - По id товара
      - По названию товара
  """
  
  """Поиск по id товара"""
  # if query.isdigit() and len(query) <= 5:
  #   return Product.objects.filter(pk=int(query))
    
  
  """Поиск по названию товара"""
  keyword = [word for word in query.split() if len(word) > 2]
  q_objects = Q()
  
  for token in keyword:
    q_objects |= Q(name__icontains=token)
    
  return Product.objects.filter(q_objects)
  # print(f'{res} nfrjq')
  
# q_search("00001")
    
    
def querySet():
  res = Product.objects.filter(Q(day__slug="thu") | Q(category__slug="all"))
  print(res)
  
# querySet()