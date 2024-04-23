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
import codecs
D = Decimal
import hashlib

def generate_token(values):
    
    sorted_values = sorted(values.items())
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
        'OrderId': str(order.id),
        'Password': password,
        'TerminalKey': terminalkey,
        'Description': f"Покупка товаров в магазине artflora38.ru"
    }
    
    token  = generate_token(values)
    print(token)
    for item in items:
        
        name = item.product.name
        unicode_str = name
        decoded_str = codecs.decode(unicode_str, 'unicode_escape').encode('latin1').decode('utf-8')
        print(decoded_str)
        # decoded_name = name.encode('utf-8').decode('unicode-escape')
        # decoded_name = name.decode('utf-8')
        # print(decoded_name)
        quantity = item.quantity
        price = str(item.price).replace('.','')
        amount = item.price * item.quantity
        amount = str(amount).replace('.','')

        
        items_arr.append(
            {
                "Name": decoded_str,
                "Price": int(price),
                "Quantity": int(quantity),
                "Amount": int(amount),
                "Tax": "none",
            }
        )
    
    dictionary = {
        "TerminalKey": terminalkey,
        "Amount": int(total_sum),
        "OrderId": str(order.id),
        "Description": "Orders",
        "SuccessURL": success_url,
        "Token": token,
        "Receipt": {
            "Phone": order.phone,
            "Email": email,
            "Taxation":"usn_income",
            "Items": items_arr,
        },
    }
    
    headers = {"Content-Type": "application/json"}
        
    payList = json.dumps(dictionary)
    # json_str = payList

    # Декодируем JSON
    decoded_json = json.loads(payList)
    
    
    try: 
        response = requests.post(
            "https://securepay.tinkoff.ru/v2/Init/", headers=headers, data=decoded_json
        )
        print(response)
        if response.status_code == 200:
            try:
                # print(response.json())
                res = response.json()
            except Exception as e:
                print("Ошибка при парсинге JSON:", e)
        else:
            print("Ошибка: невалидный статус код -", response.status_code)
    except Exception as e: 
        print("Ошибка при запросе:", e)
        
    url = res["PaymentURL"]

    # with open('data.json', 'w') as f:
    #     json.dump(payList, f)
    # print("Хуйня")
    return url
    
