from decimal import Decimal
import json
from django.shortcuts import redirect

import requests
from order.models import OrderItem

from payment.models import Tinkoff


terminalkey = "1713106439711DEMO"
taxation = "9n23lwcf2kvp01pm"

email = "saniagolovanev@gmail.com"
import logging

logger = logging.getLogger('django')

import decimal
from decimal import Decimal

D = Decimal


def create_payment(order, request):
  items_arr = []

  success_url = (
      # f'https://{request.META["HTTP_HOST"]}/orders/tinkoff_success/{order.id}/'
      f'https://artflora38.ru/orders/tinkoff_success/{order.id}/'
  )
  items = OrderItem.objects.filter(order=order)
  price_total = Decimal(0)
  for item in items:
      price_total += Decimal(item.price) * Decimal(item.quantity)

  # Формируем список позиций заказа
  items_arr = []
  for item in items:
      name = item.product.name
      quantity = Decimal(item.quantity)
      price = int(item.price)
      # price = str(price).replace(".", "")
      # print(price)
      amount = price * quantity
      items_arr.append({
          "Name": name,
          "Price": str(price),
          "Quantity": str(quantity),
          "Amount": str(amount),
          "PaymentMethod": "full_prepayment",
          "PaymentObject": "commodity",
          "Tax": "none",
      })

  # Создаем словарь для запроса оплаты
  dictionary = {
      "TerminalKey": terminalkey,
      "Amount": str(price_total),  # Передаем общую сумму заказа
      "OrderId": order.id,
      "Description": f"Покупка товаров в магазине {request.META['HTTP_HOST']}",
      "SuccessURL": success_url,
      "Receipt": {
          "Phone": order.phone,
          "EmailCompany": email,
          "Taxation": taxation,
          "Items": items_arr,
      }
  }
  # print(dictionary["Amount"])
  # print(dictionary["Receipt"]["Items"])

  headers = {"content-type": "application/json"}

  payList = json.dumps(dictionary, indent=4)

  # print(payList)
  try:
      response = requests.post(
      "https://securepay.tinkoff.ru/v2/Init", headers=headers, data=payList
  )
  except ZeroDivisionError:
      logger.error('Деление на ноль', exc_info=True)
  
  # print(response.text)
  res = response.json()
  url = res["PaymentURL"]
  # print(url)
  # with open('data.json', 'w') as f:
  #     json.dump(payList, f)

  return url
