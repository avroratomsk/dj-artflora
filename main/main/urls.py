from django.urls import path,include
from django.conf.urls.static import static
from django.contrib import admin

from main import settings

urlpatterns = [
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    # path('admin/', admin.site.urls),
    path('about/', include('home.urls')),
    path('category/', include('shop.urls')),
    path('service/', include('service.urls')),
    path('user/', include('users.urls')),
    path('reviews/', include('reviews.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('order.urls')),
    path('admin/', include('admin.urls')),
    path('', include('home.urls')),
]


if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)