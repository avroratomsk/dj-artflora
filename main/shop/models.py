from django.db import models
from django.urls import reverse

from admin.singleton_model import SingletonModel

# Дни недели с краткими ключами и полнымим наименованиями.
DAY_NAMES = (
    ('mon', 'Понедельник'),
    ('tue', 'Вторник'),
    ('wed', 'Среда'),
    ('thu', 'Четверг'),
    ('fri', 'Пятница'),
    ('sat', 'Суббота'),
    ('sun', 'Воскресенье')
)

"""Поля базы данных для настройки параметров магазина"""
class ShopSettings(SingletonModel):
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="META заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="META описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="META keywords")
  delivery = models.IntegerField(null=True, blank=True, verbose_name="Стоимость досткавки")

"""Поля базы данных для настройки параметров категории"""
class Category(models.Model):
  name = models.CharField(max_length=150, db_index=True, unique=True, verbose_name="Название категории")
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
  image = models.ImageField(upload_to="category_image", blank=True, null=True, verbose_name="Изображение категории")
  parent = models.ForeignKey('self', related_name='subcategorys', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Дочерняя категория")
  header_show = models.BooleanField(default=False, verbose_name="Отображать в шапке ?")
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="META заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="META описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="META keywords")
  menu_add = models.BooleanField(default=False, null=True, blank=True, verbose_name="Добавить в меню")
  first_block_home = models.BooleanField(default=False, null=True, blank=True, verbose_name="Вывести на главную страницу")
  
  class Meta:
    db_table = 'category' 
    verbose_name = 'Категория'
    verbose_name_plural = "Категории"
    
  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

# Продукт 
class Product(models.Model):
  name = models.CharField(max_length=150, db_index=True, verbose_name="Наименование продукта")
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
  description = models.TextField(blank=True, null=True, verbose_name="Описание")
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  image = models.ImageField(upload_to="product_iamge", blank=True, null=True, verbose_name="Изображение товара")
  price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Цена товра")
  sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Цена со скидкой")
  discount = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Скидака в %")
  quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
  category = models.ManyToManyField(Category, null=True, blank=True, verbose_name="Категории")
  composition = models.CharField(max_length=255, blank=True, null=True, verbose_name="Состав")
  diameter = models.CharField(max_length=250, blank=True, null=True, verbose_name="Диаметр")
  width = models.CharField(max_length=150, blank=True, null=True, verbose_name="Ширина")
  height = models.CharField(max_length=150, blank=True, null=True, verbose_name="Высота")
  quantity_flower = models.CharField(max_length=250, blank=True, null=True, verbose_name="Количество цветков в букете")
  quantity_purchase = models.IntegerField(default=0, verbose_name="Количество покупок")
  free_shipping = models.BooleanField(default=False, null=True, blank=True, verbose_name="Бесплатная доставка ?")
  latest = models.BooleanField(default=False, verbose_name="Новинка ?")
  status = models.BooleanField(default=True, verbose_name="Опубликовать ?")
  
  def serialize(self):
    return {
        'id': self.id,
        'name': str(self.name),
        'price': str(self.price)
    }
  
  class Meta:
    db_table = 'product' 
    verbose_name = 'Продукт'
    verbose_name_plural = "Продукты"
    ordering = ("-id",)
    
  def get_all_children_products(self):
        children = self.children.all()
        products = []
        for child in children:
            products += child.products.filter(status=True)
        return products
  
    
  def __str__(self):
    return f'{self.name} Кол-во - {self.quantity}'
    
  """ Данный метод добавляет к id нули в начале """
  def display_id(self):
    return f'{self.id:05}' #self.id:05 - сделает так чтобы id состоял из 5 символов, если не хватате символов в начало добавить 0
  
  """ Данный метод возвращает цену со скидкой"""
  def sell_price(self):
    if self.discount:
      return round(self.price - self.price * self.discount / 100, 2)
    
    return self.price
  
  def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})
    
class ProductImage(models.Model):
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="Привязка к продукту")
    src = models.ImageField(upload_to="product_iamge", null=True, blank=True, verbose_name="Дополнительны изображения")
    class Meta:
      verbose_name = 'Изображение'


class CharGroup(models.Model):
  name = models.CharField(max_length=250, verbose_name="Название группы", null=True, blank=True)
  
  def __str__(self):
    return self.name


class CharName(models.Model):
    group = models.ForeignKey(CharGroup, on_delete=models.SET_NULL, related_name='g_chars', null=True, blank=True)
    text_name = models.CharField(max_length=250, null=True, blank=True, verbose_name="Название характеристики")
    filter_add = models.BooleanField(default=False, verbose_name='Включить фильтрацию по характеристике', null=True, blank=True)
    filter_name = models.CharField(max_length=250, verbose_name='Название характеристики для фильтра (сокращенно на английском)', null=True, blank=True, unique=True)
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки', null=True, blank=True)

    def __str__(self):
        return self.text_name


class CharDefault(models.Model):
    value = models.CharField(max_length=250, verbose_name='Значение', null=True, blank=True)
    char = models.ForeignKey(CharName, on_delete=models.CASCADE, related_name='defaults', verbose_name='Характеристика', null=True, blank=True)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Значение по умолчанию'
        verbose_name_plural = 'Значения по умолчанию'

class ProductChar(models.Model):
    char_name = models.ForeignKey(CharName, on_delete=models.CASCADE, related_name='c_chars', null=True, blank=True)
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chars', null=True, blank=True)
    char_value = models.TextField()

    def __str__(self):
        return self.char_value
  
  
  
  