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
    
    dictionary = {
        "TerminalKey": terminalkey,
        "Amount": int(total_sum),
        "OrderId": str(order.id),
        "Description": f"Покупка товаров в магазине {request.META['HTTP_HOST']}",
        "SuccessURL": success_url,
        "Token": token,
        "Receipt": {
            "Phone": order.phone,
            "Email": email,
            "Taxation":"osn",
            "Items": items_arr,
        },
    }
    
    try:
        headers = {"content-type": "application/json"}
    except Exception as e:
        print(e)
    try:
        payList = json.dumps(dictionary, indent=4)
    except Exception as e:
        print(e)
    
    try: 
        response = requests.post(
            "https://rest-api-test.tinkoff.ru/v2/Init/", data=dictionary
        )
    except Exception as e: 
        print(e)
    
    try:
        res = response.json()
    except Exception as e:
        print(e)
        
    # url = res["PaymentURL"]

    # with open('data.json', 'w') as f:
    #     json.dump(payList, f)
    print("Хуйня")
    # return url
    
