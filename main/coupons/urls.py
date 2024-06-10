from django.urls import path,include
from . import views


urlpatterns = [
    path('apply/', views.coupon_apply, name='apply'),
    path('apply-to/', views.apply_to, name='apply_to'),
    path('check-coupons/', views.check_coupon_delivery, name='check_coupon_delivery'),
]