from django.urls import path

from service import views


urlpatterns = [
    path('', views.service, name="service"),
    path('<slug:slug>', views.service_detail, name="service_detail"),
]