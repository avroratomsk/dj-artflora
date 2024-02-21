from django.db import models
from django.urls import reverse


class ServicePage(models.Model):
  name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название услуги")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")

class Service(models.Model):
  name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Название услуги")
  slug = models.SlugField(max_length=150, unique=True, verbose_name="URL")
  image = models.ImageField(upload_to="services", blank=True, null=True, verbose_name="Изображение услуги")
  subtitle = models.TextField(blank=True, null=True, verbose_name="Текст под заголвком")
  status = models.BooleanField(default=True, verbose_name="Статус публикации")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  
  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
      return reverse("service_detail", kwargs={"slug": self.slug})
  
  
  