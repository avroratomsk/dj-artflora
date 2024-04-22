from decimal import Decimal
import json
from django.shortcuts import redirect

import requests
from order.models import OrderItem

from payment.models import Tinkoff


terminalkey = "1713106439711DEMO"
taxation = "9n23lwcf2kvp01pm"





email = "saniagolovanev@gmail.com"


import decimal
from decimal import Decimal

D = Decimal


def create_payment(order, request):
  print('nen')
  items_arr = []

  success_url = (
      f'https://{request.META["HTTP_HOST"]}/orders/tinkoff_success/{order.id}/'
  )
  print(success_url)
  print('1----------------------1')
  items = OrderItem.objects.filter(order=order)
  print('2----------------------2')
  print(items)
  print('3----------------------3')
  # total = str(order.summ)
  # total = total.replace(".", "")

  # print(total)

  # print(items.count())

  for item in items:
      try:
          name = item.product.name
          print('4------------------4')
      except:
          name = item.combo.name
          print('5------------------5')

      quantity = item.quantity
      print(quantity)
      print('6------------------6')
      # quantity = quantity - item.free
      # print(quantity)
      print('7------------------7')

      # if order.balls:
      #     price = item.price
      #     discount = (price / 100) * order.percent_pay
      #     price = price - discount
      #     price = str(price)
      #     price = price.replace(".", "")

      # else:
      price = item.price
      price = str(price)
      price = price.replace(".", "")
      print(price)
      print('8------------------8')
      amount = Decimal(price) * Decimal(quantity)
      amount = str(amount)
      print(amount)
      print('9------------------9')
      amount = amount.replace(".", "")
      print(amount)

      
      items_arr.append(
          {
              "Name": name,
              "Price": price,
              "Quantity": quantity,
              "Amount": amount,
              "PaymentMethod": "full_prepayment",
              "PaymentObject": "commodity",
              "Tax": "none",
          }
      )
      # print(items_arr)
      # print(order.percent_pay)
      # print('Price:')
      # print(price)
      # print('item.free')
      # print(item.free)
      # print('quantity')
      # print(quantity)
      # print('Amount:')
      # print(amount)

  # delivery_price = order.delivery_price

  # del_pr = (
  #     str(Decimal(delivery_price).quantize(D("1.00")))
  #     .replace(".", "")
  #     .replace(",", "")
  # )

  # if Decimal(delivery_price) > 0:
  #     # print(delivery_price)
  #     items_arr.append(
  #         {
  #             "Name": "Доставка",
  #             "Price": str(del_pr),
  #             "Quantity": 1,
  #             "Amount": str(del_pr),
  #             "PaymentMethod": "full_prepayment",
  #             "PaymentObject": "commodity",
  #             "Tax": "none",
  #         }
  #     )

  dictionary = {
      "TerminalKey": terminalkey,
      "Amount": 1000,
      "OrderId": order.id,
      "Description": f"Покупка товаров в магазине {request.META['HTTP_HOST']}",
      "SuccessURL": success_url,
      "Receipt": {
          "Phone": order.phone,
          "EmailCompany": email,
          "Taxation": taxation,
          "Items": items_arr,
      },
  }
  # print(dictionary)

  headers = {"content-type": "application/json"}

  payList = json.dumps(dictionary, indent=4)

  # print(payList)

  response = requests.post(
      "https://securepay.tinkoff.ru/v2/Init", headers=headers, data=payList
  )
  # print(response.text)
  res = response.json()
  print(res)
  url = res["PaymentURL"]

  with open('data.json', 'w') as f:
      json.dump(payList, f)

  return url
