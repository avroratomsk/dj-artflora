import requests
from cart.models import Cart

"""
  Функция возращает корзину пользователя и пользователя
  в зависимости от авторизации пользователя
"""
def get_cart_and_user(request):
  if request.user.is_authenticated:
    user = request.user
    cart_items = Cart.objects.filter(user=user)
  else:
    user = None
    session_key = request.session.session_key
    cart_items = Cart.objects.filter(session_key=session_key)
    
  return {"user": user, "cart_items": cart_items}