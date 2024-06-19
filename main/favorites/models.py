from django.db import models

from shop.models import Product
from users.models import User

class Favorites(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="fav_user", verbose_name="Пользователь")
  session_key = models.CharField(max_length=32, null=True, blank=True, verbose_name="ключ сессии если пользователь не авторизован")
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="fav_prod", verbose_name="Продукт")

  class Meta:
    db_table = "favorites"