from django.db import transaction
from django.forms import ValidationError
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart
from order.services import get_cart_and_user
from payment.alfabank import create_payment, get_status
from .email_send import email_send
from order.models import Order, OrderItem
from order.forms import CreateOrderForm
from django.contrib.auth.decorators import login_required
from shop.models import Product, ShopSettings
import logging
logger = logging.getLogger(__name__)

from coupons.models import Coupon

def order(request):
  ...

def order_create(request):
  """ 
    Устанавливаем значение доставки в 1 это значит что доставка нужна
    как только пользователь сменит в форме на самовывоз, то доставка перейдет в значение 0 
    и не будет учитываться.
  """
  request.session['delivery'] = 1
  
  """
    Получаем корзину в зависимости от авторизации пользователя.
    Если не авторизован, то получаем через session_key
  """
  cart_items = get_cart_and_user(request)['cart_items']
  
  form = CreateOrderForm(request.POST)
  delivery = request.session.get('delivery_summ', ShopSettings.objects.get().delivery)
  coupon_discoint = request.session.get('coupon_discoint', 0)
 
  amount_delivery = cart_items.total_price() + delivery
  total = amount_delivery - ((amount_delivery * coupon_discoint) / 100)
  
  if request.method == "POST":
    if form.is_valid():
      
      try:
        order = form.save(commit=False)
        
        order.user = get_cart_and_user(request)['user']
        cart_items = get_cart_and_user(request)['cart_items']
    
        fields = [
            'first_name', 'email', 'first_name_human',
            'phone_number_human', 'phone', 'delivery_address'
        ]
        for field in fields:
          value = request.POST.get(field)
          
          if value:  # Проверка на наличие значения
            setattr(order, field, value)
        
        # Логические поля (булевые)
        order.pickup = 'pickup' in request.POST
        order.surprise = 'surprise' in request.POST
        order.anonymous = 'anonymous' in request.POST
      
        order.save()
        for item in cart_items:
          product=item.product
          name=item.product.name
          price=item.product.sell_price()
          quantity=item.quantity
          
          orderItem  = OrderItem.objects.create(
            order = order,
            product=product,
            name=name,
            price=price,
            quantity=quantity
          )
        
        
        data = create_payment(orderItem, cart_items, request)
        payment_id = data["id"]
        confirmation_url = data["confirmation_url"]
        order.payment_id = payment_id
        order.payment_dop_info = confirmation_url
        order.save()
        return redirect(confirmation_url)
      except Exception as e:
        print(f"Error: {e}")
  
  
  context = {
    'title': 'Оформление заказа',
    'orders': True,
    'discount': coupon_discoint,
    "cart": cart_items,
    "delivery": delivery,
    "total": total
  }
  
  return render(request, "pages/orders/create.html", context)

def order_error(request):
    return render(request, "pages/orders/error.html")

def order_success(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(session_key=session_key)

    pay_id = request.GET["orderId"]

    data = get_status(pay_id)
    logger.info(data)
    if data["status"] == "0":
      order = data["order"]

      email_send(order)

      text = f"Ваш заказ принят. Ему присвоен № {order.id}."

      session_key = request.session.session_key
      cart_items = Cart.objects.filter(session_key=session_key)
      cart_items.delete()
      request.session["delivery"] = 1
      order.paid = True
      order.save()
      return redirect("/?order=True")
    else:
      order = data["order"]

      email_send(order)

      text = f"Ваш заказ принят. Ему присвоен № {order.id}."

      session_key = request.session.session_key
      cart_items = Cart.objects.filter(session_key=session_key)
      cart_items.delete()
      request.session["delivery"] = 1
      order.paid = True
      order.save()
      return redirect("/?order=True")

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

                if payment_method == "На сайте картой":
                    data = create_payment(order_item, [order_item], request)
                    payment_id = data["id"]
                    confirmation_url = data["confirmation_url"]
                    order.payment_id = payment_id
                    order.payment_dop_info = confirmation_url
                    order.save()
                    return redirect(confirmation_url)
                else:
                    email_send(order)
                    return redirect('order_succes')
            except Exception as e:
                print(e)

    context = {
        'title': 'Покупка в один клик',
        'order_form': form,
        'product': product,
        'delivery': delivery.delivery
    }

    return render(request, "pages/orders/checkout.html", context)



# def order_create(request):
#   if request.method == 'POST':
#     form = CreateOrderForm(data=request.POST)
#     print(request.POST["first_name"])
#     if form.is_valid():
#       try:
#         # with transaction.atomic():
#           if request.user.is_authenticated:
#             print("USer")
#             user = request.user
#             cart_items = Cart.objects.filter(user=user)

#             if cart_items.exists():
#                 # Создать заказ
#                 order = Order.objects.create(
#                     user=user,
#                     who_get_bouqets = form.cleaned_data['who-get-bouqets'],
#                     first_name = form.cleaned_data['first_name'],
#                     phone_number=form.cleaned_data['phone_number'],
#                     email=form.cleaned_data['email'],
#                     first_name_human=form.cleaned_data['first_name_human'],
#                     phone_number_human=form.cleaned_data['phone_number_human'],
#                     surprise=form.cleaned_data['surprise'],
#                     anonymous=form.cleaned_data['anonymous'],
#                     delivery_address=form.cleaned_data['delivery_address'],
#                     payment_option=form.cleaned_data['payment_option'],
#                 )
#                 print(f"{order} - заказ авторизованного")
#                 # Создать заказанные товары
#                 for cart_item in cart_items:
#                     product=cart_item.product
#                     name=cart_item.product.name
#                     price=cart_item.product.sell_price()
#                     quantity=cart_item.quantity


#                     if product.quantity < quantity:
#                         raise ValidationError(f'Недостаточное количество товара {name} на складе | В наличии - {product.quantity}')

#                     OrderItem.objects.create(
#                         order=order,
#                         product=product,
#                         name=name,
#                         price=price,
#                         quantity=quantity,
#                     )
#                     product.quantity -= quantity
#                     product.save()

#                 # Очистить корзину пользователя после создания заказа
#                 cart_items.delete()
#                 messages.success(request, 'Заказ оформлен!')
#                 return redirect('order_succes')
#           else:
#             session_key=request.session.session_key
#             cart_items = Cart.objects.filter(session_key=session_key)
#             print(cart_items)
#             if cart_items.exists():
#                 # Создать заказ
#                 order = Order.objects.create(
#                     phone_number=form.cleaned_data['phone_number'],
#                     delivery_address=form.cleaned_data['delivery_address'],
#                     payment_option=form.cleaned_data['payment_option'],
#                 )
#                 print(f"{order.id} - заказ сессии")
#                 # Создать заказанные товары
#                 for cart_item in cart_items:
#                     product=cart_item.product
#                     name=cart_item.product.name
#                     price=cart_item.product.sell_price()
#                     quantity=cart_item.quantity


#                     if product.quantity < quantity:
#                         raise ValidationError(f'Недостаточное количество товара {name} на складе | В наличии - {product.quantity}')

#                     OrderItem.objects.create(
#                         order=order,
#                         product=product,
#                         name=name,
#                         price=price,
#                         quantity=quantity,
#                     )
#                     product.quantity -= quantity
#                     product.save()

#                 # Очистить корзину пользователя после создания заказа
#                 cart_items.delete()
#                 messages.success(request, 'Заказ оформлен!')
#                 return redirect('order_succes')
#       except ValidationError as e:
#         print('2')
#         print(e)
#         messages.success(request, str(e))
#         return redirect('order_create')
#     else:
#       initial = {
#         # 'first_name': request.user.first_name,
#         'first_name': "",
#         # 'last_name': request.user.last_name,
#         'last_name': "",
#         }
#     form = CreateOrderForm(initial=initial)

#   context = {
#     'title': 'Home - Оформление заказа',
#     'form': form,
#     'orders': True,
#   }
#   return render(request, 'pages/orders/create.html', context)

def order_succes(request):
  return render(request, "pages/orders/success.html")