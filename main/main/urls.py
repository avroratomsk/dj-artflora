from django.urls import path,include
from django.conf.urls.static import static
from django.contrib import admin

from main import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('about/', include('home.urls')),
    path('coupons/', include('coupons.urls')),
    path('category/', include('shop.urls')),
    path('service/', include('service.urls')),
    path('user/', include('users.urls')),
    path('reviews/', include('reviews.urls')),
    path('cart/', include('cart.urls')),
    path('favorites/', include('favorites.urls')),
    path('orders/', include('order.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', include('admin.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('home.urls')),
]


if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)