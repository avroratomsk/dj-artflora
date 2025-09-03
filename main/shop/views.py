from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.http import JsonResponse
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

def delivery_zones(request):
    settings = ShopSettings.load()  # т.к. SingletonModel, используем load()

    data = {
        "deliverys": [
            {
                "hintContent": "Зона платной доставки",
                "balloonContent": "Платная доставка",
                "balloonContentHeader": "Зона платной доставки",
                "balloonContentBody": "Стоимость доставки",
                "balloonContentFooter": f"{settings.zone_one} рублей",
               "coords": [
                       [52.4226948, 103.907146],
                       [52.4851985, 103.819942],
                       [52.4420008, 103.746471],
                       [52.4163975, 103.710079],
                       [52.2927886, 104.038295],
                       [52.2599361, 103.995723],
                       [52.2236857, 104.003963],
                       [52.1916257, 104.067135],
                       [52.1434921, 103.983364],
                       [52.1527851, 104.23193],
                       [52.175587, 104.258022],
                       [52.1629207, 104.413204],
                       [52.2194686, 104.494228],
                       [52.2717321, 104.54916],
                       [52.3996004, 104.582119],
                       [52.5086668, 104.593105],
                       [52.5287725, 104.367885],
                       [52.5304476, 104.087734],
                       [52.4226948, 103.907146],
                       [52.377604, 103.964138],
                       [52.414568, 104.046535],
                       [52.433038, 104.150905],
                       [52.464923, 104.255275],
                       [52.469955, 104.392605],
                       [52.4666, 104.488735],
                       [52.407849, 104.502468],
                       [52.320417, 104.458523],
                       [52.247986, 104.414577],
                       [52.214256, 104.345913],
                       [52.195694, 104.225063],
                       [52.210038, 104.093227],
                       [52.301058, 104.050655],
                       [52.377604, 103.964138]
                     ],
                "fillColor": "#ed4543",
                "strokeColor": "#ed4543",
                "opacity": 0.2
            },
            {
                "hintContent": "Зона платной доставки",
                "balloonContent": "Платная доставка",
                "balloonContentHeader": "Зона платной доставки",
                "balloonContentBody": "Стоимость доставки",
                "balloonContentFooter": f"{settings.zone_two} рублей",
                "coords": [
                        [52.209963434003996, 104.09339927850232],
                        [52.19625214893937, 104.22987007317995],
                        [52.215657641002636, 104.34865974603146],
                        [52.247278767347474, 104.41663765130481],
                        [52.40651484701535, 104.50590156732069],
                        [52.46547708509088, 104.49182533441032],
                        [52.46883197997562, 104.39912819085575],
                        [52.464428627736886, 104.25390266595349],
                        [52.451006157007214, 104.21133064446913],
                        [52.443244415194705, 104.1843798082874],
                        [52.43485179670045, 104.15811561761353],
                        [52.42897600781463, 104.1296198290393],
                        [52.41428309107214, 104.04653572259399],
                        [52.37752926695979, 103.96413826165642],
                        [52.3395880876913, 104.00705360589467],
                        [52.30098274063468, 104.05099891839465],
                        [52.209963434003996, 104.09339927850232],
                        [52.235054616093024, 104.1852381151722],
                        [52.31592397419172, 104.14266609368758],
                        [52.37395725596692, 104.10833381829696],
                        [52.406724817634604, 104.16326545892203],
                        [52.39958525301425, 104.27999519525011],
                        [52.3726964768721, 104.33492683587512],
                        [52.338641767394016, 104.368572465758],
                        [52.3201318575174, 104.38436531243765],
                        [52.304981595568044, 104.38161873040625],
                        [52.26876820428078, 104.3816187304065],
                        [52.2443284199973, 104.36788582025012],
                        [52.22915209040576, 104.31295417962491],
                        [52.21903163973537, 104.26900886712512],
                        [52.235054616093024, 104.1852381151722]
                      ],
                "fillColor": "#1e98ff",
                "strokeColor": "#1e98ff",
                "opacity": 0.2
            },
            {
                "hintContent": "Зона платной доставки",
                "balloonContent": "Платная доставка",
                "balloonContentHeader": "Зона платной доставки",
                "balloonContentBody": "Стоимость доставки",
                "balloonContentFooter": f"{settings.zone_three} рублей",
                "coords": [
                        [52.37414277093296, 104.10902046380454],
                        [52.23566229391047, 104.18386482415612],
                        [52.22006126392441, 104.26832222161704],
                        [52.24577893510946, 104.36788582024987],
                        [52.273166533230004, 104.3809320848983],
                        [52.29338031087834, 104.38367866692955],
                        [52.322842125966154, 104.37887214837485],
                        [52.369519756955775, 104.33698677239833],
                        [52.398510621396284, 104.27930854974207],
                        [52.406070309280395, 104.16326545892171],
                        [52.37414277093296, 104.10902046380454],
                        [52.29632737916157, 104.15571235833582],
                        [52.342612574479276, 104.15021919427333],
                        [52.3787652986167, 104.1612055223983],
                        [52.389269234937956, 104.20377754388267],
                        [52.37246173120776, 104.26900886712488],
                        [52.33420070320982, 104.30952095208582],
                        [52.30222092450626, 104.34453987298423],
                        [52.2685329038379, 104.36101936517176],
                        [52.25041495438052, 104.34591316399985],
                        [52.23524071689198, 104.32737373528892],
                        [52.22680833139977, 104.26626228509363],
                        [52.23313277143478, 104.21407722649987],
                        [52.24999351820203, 104.18386482415612],
                        [52.29632737916157, 104.15571235833582]
                      ],
                "fillColor": "#1bad03",
                "strokeColor": "#1bad03",
                "opacity": 0.2
            },
            {
                "hintContent": "Зона платной доставки",
                "balloonContent": "Платная доставка",
                "balloonContentHeader": "Зона платной доставки",
                "balloonContentBody": "Стоимость доставки",
                "balloonContentFooter": f"{settings.zone_four} рублей",
                "coords": [
                        [52.29413515482308, 104.15708564935129],
                        [52.28108170691027, 104.16532539544508],
                        [52.29371413619131, 104.18523811517163],
                        [52.31686418863494, 104.26351570306223],
                        [52.30339654717476, 104.34385322747629],
                        [52.37279495720404, 104.26694893060132],
                        [52.38918222743419, 104.20446418939035],
                        [52.37951867930478, 104.16189216790599],
                        [52.34378711906572, 104.1495325487654],
                        [52.29413515482308, 104.15708564935129]
                      ],
                "fillColor": "#82cdff",
                "strokeColor": "#82cdff",
                "opacity": 0.2
            },{
                "hintContent": "Зона платной доставки",
                "balloonContent": "Платная доставка",
                "balloonContentHeader": "Зона платной доставки",
                "balloonContentBody": "Стоимость доставки",
                "balloonContentFooter": f"{settings.zone_five} рублей",
                "coords": [
                  [52.233467052911884, 104.21373390374572],
                  [52.22728021635717, 104.26621351030356],
                  [52.235574982414796, 104.32771705804261],
                  [52.250116954050895, 104.34591316399965],
                  [52.26907754580864, 104.3610193651715],
                  [52.30339654717243, 104.3431665819684],
                  [52.31665378840287, 104.26420234856991],
                  [52.29413515482074, 104.18558143792542],
                  [52.28150284620837, 104.16532539544492],
                  [52.25074910504195, 104.18317817864808],
                  [52.233467052911884, 104.21373390374572]
                ],
                "fillColor": "#56db40",
                "strokeColor": "#56db40",
                "opacity": 0.2
              }
        ]
    }

    return JsonResponse(data)
