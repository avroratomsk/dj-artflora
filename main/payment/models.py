from django.db import models

from admin.singleton_model import SingletonModel

class AlfaBank(SingletonModel):
    login = models.CharField(max_length=250, verbose_name='Логин API')
    password = models.CharField(max_length=250, verbose_name='Пароль API')

    token = models.CharField(max_length=250, verbose_name='Token', null=True, blank=True)
    
class Tinkoff(SingletonModel):
    terminalkey = models.CharField(max_length=250, verbose_name='TerminalKey')
    password = models.CharField(max_length=250, verbose_name='Пароль')

    VAT_CODES = (
       ('osn', 'общая'),
       ('usn_income', 'упрощенная (доходы)'),
       ('usn_income_outcome', 'упрощенная (доходы минус расходы)'),
       ('patent', 'патентная'),
       ('envd', 'единый налог на вмененный доход'),
       ('esn', 'единый сельскохозяйственный налог'),

    )

    taxation = models.CharField(max_length=250, verbose_name='Система налогообложения', choices=VAT_CODES)
