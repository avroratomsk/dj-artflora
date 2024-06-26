from django.urls import path

from order import views

urlpatterns = [
    path('', views.order, name="order"),
    path('create/', views.order_create, name="order_create"), 
    path('error/', views.order_error, name='order_error'),
    path('success/', views.order_success, name='order_success'),
    path('order-succes/', views.order_succes, name="order_succes"), 
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    # path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    
    # path('tinkoff_success/<int:pk>/', views.tinkoff_success, name='tinkoff_success')
    # path('cart_change/', views.cart_change, name="cart_change"), 
    # path('cart_remove/', views.cart_remove, name="cart_remove"), 
]