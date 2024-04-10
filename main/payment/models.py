from django.db import models

from admin.singleton_model import SingletonModel

class AlfaBank(SingletonModel):
    login = models.CharField(max_length=250, verbose_name='Логин API')
    password = models.CharField(max_length=250, verbose_name='Пароль API')

    token = models.CharField(max_length=250, verbose_name='Token', null=True, blank=True)
