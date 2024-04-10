from django.db import models
from shop.models import Product

from users.models import User

class OrderItemQuerySet(models.QuerySet):
  
  def total_price(self):
    return sum(cart.products_price() for cart in self)
  
  def total_quantity(self):
    if self:
      return sum(cart.quantity for cart in self)
    return 0

class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None, verbose_name="Пользователь")
  first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Имя')
  email = models.EmailField(null=True, blank=True, verbose_name='E-mail')
  created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
  phone = models.CharField(default=True, null=True, blank=True, verbose_name="Номер телефона")
  requires_delivery = models.BooleanField(null=True, blank=True, verbose_name="Нужна доставка ?")
  delivery_address = models.TextField(null=True, blank=True, verbose_name="Адрес доставки")
  payment_id = models.CharField(max_length=250, verbose_name="ID платежа", null=True, blank=True)
  payment_dop_info = models.CharField(max_length=550, verbose_name="Информация о платеже (ссылка на плптеж)", null=True, blank=True)
  pay_method = models.CharField(max_length=250, verbose_name="Способ оплаты", null=True, blank=True)
  is_paid = models.BooleanField(default=False, verbose_name="Оплачено ?")
  ORDER_STATUS = (
    ('Новый', 'Новый'),
    ('В работе', 'В работе'),
    ('Обработан', 'Обработан'),
    ('Выполнен', 'Выполнен'),
    ('Отказ', 'Отказ')
  )
  models.CharField(max_length=250, verbose_name='Статус заказа', choices=ORDER_STATUS, default='Новый',)
  
  class Meta:
    db_table="order"
    verbose_name="Заказ"
    verbose_name_plural="Заказы"
    
  def __str__(self) :
    return f"Заказа № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"
  
class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
  product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, verbose_name="Продукт")
  name = models.CharField(max_length=150, verbose_name="Имя товара")
  price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
  quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
  created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")
  
  class Meta:
    db_table = "order_item"
    verbose_name = "Проданный товара"
    verbose_name_plural = "Проданные товары"
    
  objects = OrderItemQuerySet().as_manager()
  
  """Суммарная цена продуктов(обащая цена)"""  
  def products_price(self):
    return round(self.sell_price() * self.quantity, 2)
  
  def __str__(self):
    return f"Товар {self.name} | Заказ № {self.pk}"
  
  
