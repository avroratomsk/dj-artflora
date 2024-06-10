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
        coupons = request.session.get('coupon_code', None)
        if coupon_code == coupons:
            return JsonResponse({'valid': True, 'message': 'Купон уже применен', 'coupon_discount': coupon.discount, 'status': 0})
        else:
            try:
                coupon = Coupon.objects.get(code__iexact=coupon_code, valid_from__lte=now, valid_to__gte=now, active=True)         
                # if coupon.valid_to < datetime.now() or not coupon.active:
                #     return JsonResponse({'valid': False, 'message': 'Купон недействителен или срок действия истек'})
                
                # Сохраняем купон в сессию
                request.session['coupon_discoint'] = coupon.discount
                request.session['coupon_code'] = coupon.code
                print(coupon.discount)

                return JsonResponse({'valid': True, 'message': 'Купон успешно применен', 'coupon_discount': coupon.discount, 'status': 1})
            
            except Coupon.DoesNotExist:
                return JsonResponse({'valid': False, 'message': 'Купон не найден', 'status': -1})

    return JsonResponse({'valid': False, 'message': 'Неверный метод запроса', 'status': -1})

def check_coupon_delivery(request):
    delivery = request.session.get('delivery_summ')
    coupon_sum = request.session.get('coupon_discoint')
    
    return JsonResponse({'delivery': delivery, 'coupon_sum': coupon_sum, 'status': 1})