from decimal import Decimal
import json
from django.shortcuts import redirect

import requests
from order.models import OrderItem

from payment.models import Tinkoff


terminalkey = "1713106439711DEMO"
password = "9n23lwcf2kvp01pm"

email = "saniagolovanev@gmail.com"

from decimal import Decimal

D = Decimal
import hashlib

def generate_token(values):
    
    sorted_values = sorted(values.items())
    # Получить только значения и объединить их
    combined_values = ''.join(str(value) for key, value in sorted_values)
    
    hash_object = hashlib.sha256(combined_values.encode('utf-8'))
    token = hash_object.hexdigest()
    
    return token

def create_payment(order, request):
    items_arr = []

    success_url = (
        f'https://{request.META["HTTP_HOST"]}/orders/tinkoff_success/{order.id}/'
    )

    items = OrderItem.objects.filter(order=order)
    total_sum = 0
    
    for item in items:
        total_sum += item.price * item.quantity
    total_sum = str(total_sum).replace(".", "")
    
    values = {
        'Amount': total_sum,
        'OrderId': f"{order.id}",
        'Password': password,
        'TerminalKey': terminalkey,
        'Description': f"Покупка товаров в магазине artflora38.ru"
    }
    
    token  = generate_token(values)
    
    for item in items:
        
        name = item.product.name
        quantity = item.quantity
        price = str(item.price).replace('.','')
        amount = item.price * item.quantity
        amount = str(amount).replace('.','')

        
        items_arr.append(
            {
                "Name": name,
                "Price": int(price),
                "Quantity": int(quantity),
                "Amount": int(amount),
                "Tax": "none",
            }
        )
    
    # dictionary = {
    #     "TerminalKey": terminalkey,
    #     "Amount": int(total_sum),
    #     "OrderId": str(order.id),
    #     "Description": "Orders",
    #     "SuccessURL": success_url,
    #     "Token": token,
    #     "Receipt": {
    #         "Phone": order.phone,
    #         "Email": email,
    #         "Taxation":"usn_income",
    #         "Items": items_arr,
    #     },
    # }
    
    dictionary = {
        "TerminalKey": terminalkey,
        "Amount":140000,
        "OrderId":"21050",
        "Description":"Подарочная карта на 1000 рублей",
        "Token": token,
        "DATA": {
        "Phone":"+71234567890",
        "Email":"a@test.com"
        },
        "Receipt": {
        "Email":"a@test.ru",
        "Phone":"+79031234567",
        "Taxation":"osn",
        "Items": [
        {
        "Name":"Наименование товара 1",
        "Price":10000,
        "Quantity":1.00,
        "Amount":10000,
        "Tax":"vat10",
        "Ean13":"303130323930303030630333435"
        },
        {
        "Name":"Наименование товара 2",
        "Price":20000,
        "Quantity":2.00,
        "Amount":40000,
        "Tax":"vat20"
        },
        {
        "Name":"Наименование товара 3",
        "Price":30000,
        "Quantity":3.00,
        "Amount":90000,
        "Tax":"vat10"
        }
        ]
        }
        }

    
    try:
        headers = {"Content-Type": "application/json"}
    except Exception as e:
        print(e)
        
    
    payList = json.dumps(dictionary, indent=4)
    # print(payList)
    
    
    try: 
        response = requests.post(
            "https://rest-api-test.tinkoff.ru/v2/Init/", headers=headers, data=payList
        )
        if response.status_code == 200:
            try:
                print(response.json())
                # res = response.json()
            except Exception as e:
                print("Ошибка при парсинге JSON:", e)
        else:
            print("Ошибка: невалидный статус код -", response.status_code)
    except Exception as e: 
        print("Ошибка при запросе:", e)
        
    # url = res["PaymentURL"]

    # with open('data.json', 'w') as f:
    #     json.dump(payList, f)
    # print("Хуйня")
    return True
    
