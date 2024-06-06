from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExists:
            request.session['coupon_id'] = None
    return redirect(request.META.get('HTTP_REFERER'))
  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Coupon
from datetime import datetime
import json
from cart.models import Cart

@csrf_exempt
def apply_to(request):
    now = timezone.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        coupon_code = data.get('couponCode')
        try:
            coupon = Coupon.objects.get(code__iexact=coupon_code, valid_from__lte=now, valid_to__gte=now, active=True)
            if request.user.is_authenticated:
                cart = Cart.objects.filter(user=request.user)
                print(cart.coupon)
            else:
                cart = Cart.objects.filter(session_key=request.session.session_key)
                
            # if coupon.valid_to < datetime.now() or not coupon.active:
            #     return JsonResponse({'valid': False, 'message': 'Купон недействителен или срок действия истек'})
            
            # Сохраняем купон в сессию
            
            request.session['coupon_id'] = coupon.id

            return JsonResponse({'valid': True, 'message': 'Купон успешно применен', 'coupon_discount': coupon.discount})
        
        except Coupon.DoesNotExist:
            return JsonResponse({'valid': False, 'message': 'Купон не найден'})

    return JsonResponse({'valid': False, 'message': 'Неверный метод запроса'})
