from django.db import models

from shop.models import Product

class SEO(models.Model):
  meta_h1 = models.CharField(max_length=250, null=True, blank=True, db_index=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=250, null=True, blank=True, db_index=True, verbose_name="META заголовок")
  meta_description = models.TextField(null=True, blank=True, db_index=True, verbose_name="META описание")
  meta_keywords = models.CharField(max_length=250, null=True, blank=True, db_index=True, verbose_name="META слова")
  verification_yandex = models.CharField(max_length=200, null=True, blank=True, db_index=True, verbose_name="Код верификации яндекс консоли")
  verification_google = models.CharField(max_length=200, null=True, blank=True, db_index=True, verbose_name="Код верификации гугл консоли")
  product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name="product", verbose_name="Связанный продукт")
  
  class Meta:
    db_table = 'seo'
  
  def __str__(self):
    return self.meta_h1
