from django.db import transaction
from django.forms import ValidationError
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from cart.models import Cart
from order.services import get_cart_and_user
from payment.alfabank import create_payment, get_status
from .email_send import email_send
from order.models import Order, OrderItem
from order.forms import CreateOrderForm
from django.contrib.auth.decorators import login_required
from shop.models import Product, ShopSettings
import logging
from .telegram import order_telegram, send_message
logger = logging.getLogger(__name__)

from coupons.models import Coupon

def order(request):
  ...

# from django.db import transaction
# from django.forms import ValidationError
# from django.contrib import messages
# from django.shortcuts import get_object_or_404, redirect, render
# from cart.models import Cart
# from order.services import get_cart_and_user
# from payment.alfabank import create_payment, get_status
# from .email_send import email_send
# from order.models import Order, OrderItem
# from order.forms import CreateOrderForm
# from django.contrib.auth.decorators import login_required
# from shop.models import Product, ShopSettings
# import logging
# logger = logging.getLogger(__name__)
# from datetime import datetime
# from coupons.models import Coupon

def order_create(request):
#       with open("/home/a/avroraweb/irk-artlora.ru/public_html/debug.log", "a", encoding="utf-8") as f:
#           f.write(f"order_create HIT, method={request.method}, session={dict(request.session)}\n")
      if request.method == "GET":
          # Если доставки в сессии нет — ставим по умолчанию
          if "delivery_summ" not in request.session:
              request.session["delivery_summ"] = ShopSettings.objects.get().delivery

      """
      Создание заказа из корзины, с поддержкой выбора доставки, скидки и способа оплаты
      """
      # Получаем корзину и пользователя
      cart_items = get_cart_and_user(request)['cart_items']
      form = CreateOrderForm(request.POST)

#       # Сумма доставки из сессии или из настроек магазина по умолчанию
#       delivery = request.session.get('delivery_summ', ShopSettings.objects.get().delivery)
#
#       # Скидка из купона (если применён)
#       coupon_discount = request.session.get('coupon_discoint', 0)
#
#       # Общая сумма с доставкой
#       amount_delivery = cart_items.total_price() + delivery
#
#       # Учитываем скидку
#       total = amount_delivery - ((amount_delivery * coupon_discount) / 100)
      delivery = request.session.get('delivery_summ', ShopSettings.objects.get().delivery)
      coupon_discount = request.session.get('coupon_discoint', 0)  # исправил название ключа

      subtotal = cart_items.total_price()  # сумма товаров
      discount_amount = (subtotal * coupon_discount) / 100  # скидка в рублях
      after_discount = subtotal - discount_amount
      total = after_discount + delivery


      if request.method == "POST":
          if form.is_valid():
              try:
                  order = form.save(commit=False)

                  # Привязываем пользователя (если авторизован)
                  order.user = get_cart_and_user(request)['user']
                  cart_items = get_cart_and_user(request)['cart_items']

                  # Заполняем поля из формы (не все есть в модели, часть через request.POST)
                  fields = [
                      'first_name', 'email', 'first_name_human',
                      'phone_number_human', 'phone', 'delivery_address', 'delivery_date', 'delivery_time'
                  ]
                  for field in fields:
                      value = request.POST.get(field)
                      if value:
                        setattr(order, field, value)

                  # Булевые переключатели
                  order.pickup = 'pickup' in request.POST
                  order.surprise = 'surprise' in request.POST
                  order.anonymous = 'anonymous' in request.POST
                  order.message = request.POST.get('message') or ''


                  # ⚠️ Новый блок — сохраняем выбранный способ оплаты
                  payment_method = request.POST.get('payment_option', '')
                  order.pay_method = payment_method  # или order.payment_option, если поле так называется в модели

                  order.save()
                  # Добавляем товары в заказ
                  for item in cart_items:
                      product = item.product
                      name = product.name
                      price = product.sell_price()
                      quantity = item.quantity

                      OrderItem.objects.create(
                          order=order,
                          product=product,
                          name=name,
                          price=price,
                          quantity=quantity
                      )

                    # Проверяем способ оплаты
#                   if payment_method == "На сайте картой":
                  data = create_payment(order, cart_items, request)
                  payment_id = data["id"]
                  confirmation_url = data["confirmation_url"]

                  if Order.objects.filter(payment_id=payment_id).exists():
                      logger.error(f"[order_create] Duplicate payment_id detected before saving: {payment_id}")
                      messages.error(request, "Ошибка при создании платежа. Попробуйте снова.")
                      order.delete()
                      return redirect("order_create")

                  order.payment_id = payment_id
                  order.payment_dop_info = confirmation_url
                  order.save()
                  return redirect(confirmation_url)
#                   else:
                    # Иначе — подтверждаем заказ без оплаты онлайн
#                     email_send(order)
#                       order_telegram(order)
#                     cart_items.delete()
#                     request.session["delivery"] = 1
#                     order.is_paid = True
#                     order.save()
#                     return redirect('order_succes')

              except Exception as e:
                  print(f"Error: {e}")
                  messages.error(request, "Произошла ошибка при оформлении заказа.")

      context = {
          'title': 'Оформление заказа',
          'orders': True,
          'discount': coupon_discount,
          "cart": cart_items,
          "delivery": delivery,
          "total": total,
          "form": form
      }

      return render(request, "pages/orders/create.html", context)

def order_error(request):
    return render(request, "pages/orders/error.html")

def order_success(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(session_key=session_key)

    pay_id = request.GET.get("orderId")
    if not pay_id:
        logger.error("No orderId in request")
        return render(request, "pages/orders/error.html")

    data = get_status(pay_id)
    logger.info(f"[order_success] get_status({pay_id}) -> {data}")
    order = data.get("order")

    if not order:
        logger.error("No order returned from get_status")
        return render(request, "pages/orders/error.html")

    logger.info(f"[order_success] Order #{order.id}, status: {data.get('order_status')}, code: {data.get('status')}")

    if data["status"] == "0":
#         if not order.is_paid:  # только если ещё не оплачен
        order.is_paid = True
        order.save()

        logger.info(f"[order_success] Sending email for order #{order.id}")
        try:
          email_send(order)
          logger.info(f"[order_success] Email send completed for order #{order.id}")
          # order_telegram(order)
        except:
          logger.error(f"[order_success] Email send FAILED for order #{order.id}: {e}")

        cart_items = Cart.objects.filter(session_key=session_key)
        cart_items.delete()
        request.session["delivery"] = 1

        return redirect("/?order=True")
    else:
        logger.warning(f"Payment failed for order {order.id}. Status: {data['status']}")
        # не перезаписывай order.is_paid = False без надобности
        return render(request, "pages/orders/error.html")


def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = CreateOrderForm(request.POST or None)
    delivery = ShopSettings.objects.get()

    if request.method == "POST":
        payment_method = request.POST['payment_option']
        if form.is_valid():
            try:
                order = form.save(commit=False)
                order.user = request.user if request.user.is_authenticated else None
                order.first_name = request.POST.get('first_name', '')
                order.email = request.POST.get('email', '')
                order.phone = request.POST.get('phone', '')
                order.delivery_address = request.POST.get('delivery_address', '')
                order.pay_method = payment_method
                order.save()

                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    name=product.name,
                    price=product.price,
                    quantity=1
                )

#                 if payment_method == "На сайте картой":
                data = create_payment(order_item, [order_item], request)
                payment_id = data["id"]
                confirmation_url = data["confirmation_url"]
                order.payment_id = payment_id
                order.payment_dop_info = confirmation_url
                order.save()
                return redirect(confirmation_url)
#                 else:
#                     email_send(order)
#                     order_telegram(order)
#                     return redirect('order_succes')
            except Exception as e:
                print(e)

    context = {
        'title': 'Покупка в один клик',
        'order_form': form,
        'product': product,
        'delivery': delivery.delivery
    }

    return render(request, "pages/orders/checkout.html", context)


def order_succes(request):
  return render(request, "pages/orders/success.html")