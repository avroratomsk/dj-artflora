from django.db import models
from django.urls import reverse

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

# Категория
class Category(models.Model):
  name = models.CharField(max_length=150, db_index=True, unique=True, verbose_name="Название категории")
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
  image = models.ImageField(upload_to="category_image", blank=True, null=True, verbose_name="Изображение категории")
  parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Дочерняя категория")
  header_show = models.BooleanField(default=False, verbose_name="Отображать в шапке ?")
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="META заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="META описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="META keywords")
  menu_add = models.BooleanField(default=False, null=True, blank=True, verbose_name="Добавить в меню")
  
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
  category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, default=None, verbose_name='День недели')
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
    
class CharName(models.Model):
  char_name = models.CharField(max_length=250, verbose_name="Название характеристки")

class ProductSpecification(models.Model):
  product = models.ManyToManyField(Product, related_name='character', verbose_name="Связь с продуктом")
  char_name = models.ForeignKey(CharName, on_delete=models.CASCADE, related_name='chars', null=True, blank=True)
  value = models.CharField(max_length=100, verbose_name="Значение")
  
  class Meta:
    db_table = 'characteristics'
    
  def __str__(self):
     return self.name
  
  
  
  