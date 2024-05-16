from decimal import Decimal
from django.shortcuts import render
import requests
from .models import AlfaBank
from order.models import Order
from shop.models import Product

login = "i-artflora38_ru-api"
# password = "i-artflora38*?1"
password = "}w~TlFdYeE3"
# token = AlfaBank.objects.get().token


gateway_url = ""

def create_payment(order, cart, request):
    returnUrl = "https://" + request.META["HTTP_HOST"] + "/orders/order-succes/"
    failUrl = "https://" + request.META["HTTP_HOST"] + "/orders/order-error/"

    def dec_to_cop(price):
        res = str(round(price, 2))
        res_filter = res.replace(",", "").replace(".", "")
        return res_filter

    items = []
    count = 1
    for item in cart:
        product = Product.objects.get(id=item.product.id)
        i = {
            "positionId": count,
            "name": product.name,
            "quantity": {"value": int(item.quantity), "measure": "шт"},
            "itemAmount": dec_to_cop(Decimal(item.product.sell_price()) * item.quantity),
            "itemCode": product.id,
            "itemPrice": dec_to_cop(Decimal(item.product.sell_price())),
        }
        count += 1
        items.append(i)
    
    sum = 0
    for item in items:
        sum += int(item["itemAmount"])
        
    post_data = {
        "userName": login,
        "password": password,
        "orderNumber": order.id,
        "amount": sum,
        "returnUrl": returnUrl,
        "failUrl": failUrl,
        "cartItems": items,
    }
    
    r = requests.post("https://ecom.alfabank.ru/api/rest/register.do", post_data)

    try:
        confirmation_url = r.json()["formUrl"]
        pay_id = r.json()["orderId"]
    except:
        error = r.json()["errorCode"]
        confirmation_url = "/pay-error/" + error + "/"
        pay_id = "0"

    data = {"id": pay_id, "confirmation_url": confirmation_url}
    sum = 0
    return data


def get_status(pay_id):
    order = Order.objects.get(payment_id=pay_id)

    post_data = {
        "userName": login,
        "password": password,
        "orderId": pay_id,
        "orderNumber": order.id,
    }

    r = requests.post(
        "https://ecom.alfabank.ru/api/rest/getOrderStatusExtended.do", post_data
    )
    # print(r.json())

    status = r.json()["errorCode"]

    data = {"status": status, "order": order}

    return data

