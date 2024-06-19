from django.urls import path,include
from django.conf.urls.static import static
from django.contrib import admin

from favorites import views

urlpatterns = [
    path("", views.favorites, name="favorites"),
    path("favorites-toggle/", views.favorites_toggle, name="favorites_toggle"),
    path("check/", views.favorites_check, name="favorites_check"),
]
