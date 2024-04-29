from decimal import Decimal
import json
from django.shortcuts import redirect

import requests
from order.models import OrderItem

from payment.models import Tinkoff


terminalkey = "1713419929838"
password = "j9lrf7t4z7362bld"

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
    for item in items:
        
        name = item.product.name
        unicode_str = name
        decoded_str = codecs.decode(unicode_str, 'unicode_escape').encode('latin1').decode('utf-8')
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
    print(payList)
    
    response = requests.post(
        "https://securepay.tinkoff.ru/v2/Init/", headers=headers, data=payList
    )
    res = response.json()
    print('------------')
    url = res["PaymentURL"]
    print(url)

    # with open('data.json', 'w') as f:
    #     json.dump(payList, f)
    # print("Хуйня")
    return url
    
