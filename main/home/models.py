from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

from admin.singleton_model import SingletonModel

class BaseSettings(SingletonModel):
  logo  = models.ImageField(upload_to="base-settings", blank=True, null=True, verbose_name="Логотип")
  phone_one = models.CharField(max_length=50, blank=True, null=True, db_index=True, verbose_name="Номер телефона")
  phone_two = models.CharField(max_length=50, blank=True, null=True, db_index=True, verbose_name="Номер телефона")
  time_work = models.CharField(max_length=250, blank=True, null=True, db_index=True, verbose_name="Время работы")
  email = models.EmailField(max_length=250, blank=True, null=True, db_index=True, verbose_name="Email")
  address_one = models.CharField(max_length=250, blank=True, null=True, verbose_name="Адрес первого филлиала")
  address_two = models.CharField(max_length=250, blank=True, null=True, verbose_name="Адрес второго филлиала")
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  

class HomeTemplate(SingletonModel):
  banner = models.ImageField(upload_to="home-page", blank=True, null=True, verbose_name="Картинка главной страницы")
  meta_h1 = models.CharField(max_length=250, blank=True, null=True, verbose_name="Заголовок первого уровня")
  untitle = models.CharField(max_length=250, blank=True, null=True, verbose_name="Надзаголовок")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  about_text = models.TextField(null=True, blank=True, verbose_name="О компании")
  about_image = models.ImageField(upload_to="home-page", null=True, blank=True, verbose_name="О компании картинка")
  
class Stock(models.Model):
  """Model"""
  title = models.CharField(max_length=250, blank=True, null=True, verbose_name="Название акции")
  description = models.TextField(blank=True, null=True, verbose_name="Описание акции")
  validity = models.DateTimeField(blank=True, null=True, help_text="После окончания акции, она перейдет в состояние не активна", verbose_name="Срок дейстия акции")
  status = models.BooleanField(default=True, verbose_name="Статус публикации")
  image = models.ImageField(upload_to="stock", null=True, blank=True, verbose_name="ФОтография акции")
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")

  def get_absolute_url(self):
      return reverse("stock_detail", kwargs={"slug": self.slug})
