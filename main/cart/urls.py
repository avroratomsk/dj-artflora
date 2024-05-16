from django.urls import path

from cart import views

urlpatterns = [
    path('cart_add/', views.cart_add, name="cart_add"), 
    path('cart_change/', views.cart_change, name="cart_change"), 
    path('cart_remove/', views.cart_remove, name="cart_remove"),
    path('set_delivery/<int:value>/', views.set_delivery, name='set_delivery'),
    path('delivery_summ/<int:value>/', views.delivery_summ, name='delivery_summ'),
    path('', views.cart, name="cart"),
]