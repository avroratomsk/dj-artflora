from decimal import Decimal
from django.shortcuts import render
import requests
from .models import AlfaBank
from order.models import Order
from shop.models import Product
import uuid


login = "i-artflora38_ru-api"
# password = "i-artflora38*?1"
password = "D~8Z{3mw"
# token = AlfaBank.objects.get().token
import logging
logger = logging.getLogger(__name__)

gateway_url = ""

def create_payment(order, cart, request):
    returnUrl = "https://" + request.META["HTTP_HOST"] + "/orders/success/"
    failUrl = "http://" + request.META["HTTP_HOST"] + "/orders/error/"

    # Генерируем уникальный UUID для платежа
    payment_uuid = str(uuid.uuid4())

    # Используем его как часть номера заказа
    order_number = f"{order.id}-{payment_uuid[:8]}"

    delivery = request.session.get('delivery_summ')
    delivery = int("{0:.2f}".format(delivery).replace('.',''))

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
        "orderNumber": order_number,
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
    """
    Найти заказ по payment_id с fallback-логикой
    """
    logger.info(f"[get_status] Searching for payment_id: {pay_id}")

    # Сначала ищем по payment_id (основной способ)
    orders = Order.objects.filter(payment_id=pay_id)

    if orders.exists():
        logger.info(f"[get_status] Found {orders.count()} order(s) by payment_id")
        order = orders.filter(is_paid=False).first() or orders.latest('id')
        logger.info(f"[get_status] Selected order ID: {order.id}")
    else:
        # FALLBACK: пробуем найти заказ по ID из orderNumber
        logger.warning(f"[get_status] No orders found by payment_id, trying fallback...")

        # Парсим orderNumber (формат: "123-uuid")
        try:
            # Получаем статус от Альфа-Банка чтобы узнать orderNumber
            post_data = {
                "userName": login,
                "password": password,
                "orderId": pay_id,
            }
            r = requests.post("https://ecom.alfabank.ru/api/rest/getOrderStatus.do", post_data)
            response_data = r.json()

            order_number = response_data.get("orderNumber", "")
            if order_number and "-" in order_number:
                order_id = int(order_number.split("-")[0])  # Берем часть до дефиса
                order = Order.objects.filter(id=order_id).first()
                if order:
                    logger.info(f"[get_status] Found order by ID fallback: {order.id}")
                    # Обновляем payment_id для будущих запросов
                    order.payment_id = pay_id
                    order.save()
                    logger.info(f"[get_status] Updated payment_id for order {order.id}")
                else:
                    logger.error(f"[get_status] No order found by ID: {order_id}")
                    return {"status": "-1", "order": None}
            else:
                logger.error(f"[get_status] Invalid orderNumber format: {order_number}")
                return {"status": "-1", "order": None}

        except Exception as e:
            logger.error(f"[get_status] Fallback search failed: {e}")
            return {"status": "-1", "order": None}

    # Получаем актуальный статус от банка
    post_data = {
        "userName": login,
        "password": password,
        "orderId": pay_id,
    }

    r = requests.post("https://ecom.alfabank.ru/api/rest/getOrderStatus.do", post_data)
    response_data = r.json()

    status = response_data.get("errorCode")
    order_status = response_data.get("OrderStatus")

    logger.info(f"[get_status] Order {order.id} — Status: {order_status}, ErrorCode: {status}")
    data = {"status": status, "order": order, "order_status": order_status}
    return data

