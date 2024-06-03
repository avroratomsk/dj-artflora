from django.db import transaction
from django.forms import ValidationError
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart
from payment.alfabank import create_payment, get_status
from .email_send import email_send
from order.models import Order, OrderItem
from order.forms import CreateOrderForm
from django.contrib.auth.decorators import login_required
from shop.models import Product, ShopSettings
import logging
logger = logging.getLogger(__name__)

def order(request):
  ...
  
def order_create(request):
  form = CreateOrderForm(request.POST)
  
  # Получаем стоимость минимальной доставки
  delivery = ShopSettings.objects.get()
  # request.session['delivery'] = 1
  if request.method == "POST":
    """Получаем способ оплаты и в зависимости от метода оплаты строим логику ниже"""
    payment_method = request.POST['payment_option']
    if form.is_valid():
      try:
        order = form.save(commit=False)
        if request.user.is_authenticated:
          user = request.user
          order.user = user
          # Получаем корзину пользователя если он авторизован
        else:
          order.user = None
          # Получаем корзину пользователя если он не авторизован по ключу сессии
          session_key = request.session.session_key
          cart_items = Cart.objects.filter(session_key=session_key)
          
          try: 
            first_name = request.POST['first_name']
            order.first_name = first_name
          except:
            pass          
          try:
            email = request.POST['email']
            order.email = email
          except:
            pass
          
          try:
            first_name_human = request.POST['first_name_human']
            order.first_name_human = first_name_human
          except:
            pass
          
          try:
            phone_number_human = request.POST['phone_number_human']
            order.phone_number_human = phone_number_human
          except:
            pass
          
          try:
            pickup = request.POST['pickup']
            order.pickup = True
          except:
            pass
          
          try:
            surprise = request.POST['surprise']
            order.surprise = True
          except:
            pass
          
          try:
            anonymous = request.POST['anonymous']
            order.anonymous = True
          except:
            pass
          
          try:
            phone = request.POST['phone']
            order.phone = phone
          except:
            pass
          
          try:
            delivery_address = request.POST['delivery_address']
            order.delivery_address = delivery_address
          except: 
            pass
          
          try:
            pay_method = request.POST['payment_option']
            order.pay_method = pay_method
          except: 
            pass
        
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
          
          if payment_method == "На сайте картой":
              data = create_payment(orderItem, cart_items, request)
              payment_id = data["id"]
              confirmation_url = data["confirmation_url"]
              order.payment_id = payment_id
              order.payment_dop_info = confirmation_url
              order.save()
              return redirect(confirmation_url)
          else:
            email_send(order)
            cart_items.delete()
            return redirect('order_success')
      except Exception as e:
        print(e)
  
  # cart = request.context['cart_my']
  
  session_key = request.session.session_key
  cart_items = Cart.objects.filter(session_key=session_key)
  context = {
    'title': 'Оформление заказа',
    'orders': True,
    "cart": cart_items,
    "delivery": delivery.delivery
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
from django.db.models import Sum

def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order = Order.objects.create(user=request.user)
    OrderItem.objects.create(order=order, product=product, price=product.price, quantity=1)
    order.total_price = order.items.aggregate(total=Sum('price'))['total'] or 0
    order.save()
    return redirect('checkout', order_id=order.id)
  
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        form = CreateOrderForm(request.POST, instance=order)
        if form.is_valid():
            order.save()
            return redirect('order_success', order_id=order.id)
    else:
        form = CreateOrderForm(instance=order)
    return render(request, 'pages/orders/checkout.html', {'form': form, 'order': order})

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