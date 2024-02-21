from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  pass
  # image = models.ImageField(upload_to="user_image", blank=True, null=True)
  
  # class Meta:
  #   db_table = 'user'
  #   verbose_name = "Пользователь"
  #   verbose_name_plural = "Пользователи"
  #   ordering = ("id",)
  
  
  # def __str__(self):
  #   return self.username