from django.db import transaction
from django.forms import ValidationError
from django.contrib import messages
from django.shortcuts import redirect, render
from cart.models import Cart
from payment.tinkoff import create_payment
from .email_send import email_send
from order.models import Order, OrderItem
from order.forms import CreateOrderForm
from django.contrib.auth.decorators import login_required

def order(request):
  ...

def order_create(request):
  form = CreateOrderForm(request.POST)
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
              data = create_payment(order,  request)
                # payment_id = data["id"]
                # confirmation_url = data["confirmation_url"]

                # order.payment_id = payment_id
                # order.payment_dop_info = confirmation_url
                # order.save()
                # print(data['path'])
                # print(cart_items)
                # return redirect(confirmation_url)
          else:
            email_send(order)
            cart_items.delete()
            return redirect('order_succes')
      except Exception as e:
        print(e)
  
  # cart = request.context['cart_my']
  
  session_key = request.session.session_key
  cart_items = Cart.objects.filter(session_key=session_key)
  context = {
    'title': 'Home - Оформление заказа',
    'orders': True,
    "cart": cart_items
  }
      
  return render(request, "pages/orders/create.html", context)

def order_error(request):
    return render(request, "orders/order/error.html")

def order_success(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(session_key=session_key)

    pay_id = request.GET["orderId"]

    data = get_status(pay_id)

    if data["status"] == "0":
        order = data["order"]

        email_send(order)

        text = f"Ваш заказ принят. Ему присвоен № {order.id}."

        session_key = request.session.session_key
        cart_items = Cart.objects.filter(session_key=session_key)
        request.session["delivery"] = 1
        order.paid = True

        order.save()

        return redirect("/?order=True")

    else:
        return redirect("order_error")

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
