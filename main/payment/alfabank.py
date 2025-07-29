from decimal import Decimal
from django.shortcuts import render
import requests
from .models import AlfaBank
from order.models import Order
from shop.models import Product
import logging

logger = logging.getLogger(__name__)

login = "i-artflora38_ru-api"
# password = "i-artflora38*?1"
password = "D~8Z{3mw"
# token = AlfaBank.objects.get().token


gateway_url = ""

def create_payment(order, cart, request):
    returnUrl = "https://" + request.META["HTTP_HOST"] + "/orders/success/"
    failUrl = "http://" + request.META["HTTP_HOST"] + "/orders/error/"
    isDelivery = request.session.get('delivery')
    if isDelivery == 1:
      delivery = request.session.get('delivery_summ')
      delivery = int("{0:.2f}".format(delivery).replace('.',''))
    else: 
      delivery = 0
    
    isCoupon = request.session.get('coupon_code')
    
    if isCoupon:
        coupon_discount = request.session.get('coupon_discoint')
    else:
        coupon_discount = 0
        
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
    
    sum  = 0
    
    for item in items:
        sum += int(item["itemAmount"])
        
    sum += delivery
    sum = sum - ((sum * coupon_discount) / 100)
    
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
  try:
    order = Order.objects.get(payment_id=pay_id)

    post_data = {
        "userName": login,
        "password": password,
        "orderId": pay_id,
        "orderNumber": order.id,
    }

    r = requests.post(
        "https://ecom.alfabank.ru/api/rest/getOrderStatus.do", post_data
    )

    error_code = r.json()["errorCode"]
    order_status = r.json()["OrderStatus"]
    logger.info(f"[AlfaBank] Order {order.id} — Status: {order_status}, ErrorCode: {error_code}")

    data = {
         "error": error_code,
         "status": order_status,
         "order": order,
     }

    return data
  except Exception as e:
    return {"status": "error", "order": None}

