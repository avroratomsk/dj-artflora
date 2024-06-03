from django.urls import path

from . import views


urlpatterns = [
    path('', views.admin, name="admin"),
    
    #URl - отвечающие за загрузку данных
    path('upload-goods/', views.upload_goods, name="upload_goods"),
    path('upload-succes/', views.upload_succes, name="upload-succes"),
    
    #URl - отвечающие за отображение категорий, редактирование и удаление категории
    path('category/', views.admin_category, name='admin_category'),
    path('category/add/', views.category_add, name='category_add'),
    path('category/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    #URl - отвечающие за отображение дня недели, редактирование и удаление дня недели
    path('days/', views.day_product, name='admin_day'),
    path('days/add/', views.day_add, name='days_add'),
    path('days/edit/<int:pk>/', views.day_edit, name='days_edit'),
    # path('days/delete/<int:pk>/', views.day_delete, name='days_delete'),
    
    #URl - отвечающие за отображение товаров, редактирование и удаление товара
    path('shop/', views.admin_shop, name='admin_shop'),
    path('product/', views.admin_product, name='admin_product'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('product/delete/<int:pk>/', views.product_delete, name='product_delete'),
    
    #URl - отвечающие за отображение характиристик, редактирование и удаление характеристик
    #URl - отвечающие за отображение характиристик, редактирование и удаление характеристик
    path('char/', views.admin_char, name='admin_char'),
    path('char/char-add/', views.char_add, name='char_add'),
    path('char/char-edit/<int:pk>', views.char_edit, name='char_edit'),
    path('char/char-delete/<int:pk>', views.char_delete, name='char_delete'),
    
    
    path('char/group/add/', views.char_group_add, name='char_group_add'),
    path('char/group/edit/<int:pk>', views.char_group_edit, name='char_group_edit'),
    path('char/group/delete/<int:pk>', views.char_group_delete, name='char_group_delete'),
    
    #URl - отвечающие за отображение филлиалов, редактирование и удаление филлиала
    path('fillial/', views.admin_fillial, name='admin_fillial'),
    path('fillial/add/', views.fillial_add, name='fillial_add'),
    path('fillial/edit/<int:pk>/', views.fillial_edit, name='fillial_edit'),
    # path('fillial/delete/<int:pk>/', views.fillial_delete, name='fillial_delete'),
    
    #URl - отвечающие за отображение отзывов, редактирование и удаление отзывов
    path('admin-reviews/', views.admin_reviews, name='admin_reviews'),
    path('admin-reviews/add/', views.admin_reviews_add, name='admin_reviews_add'),
    path('admin-reviews/edit/<int:pk>/', views.admin_reviews_edit, name='admin_reviews_edit'),
    # path('admin_reviews/delete/<int:pk>/', views.admin_reviews_delete, name='admin_reviews_delete'),
    
    #URl - отвечающие за отображение акций, редактирование и удаление акций
    path('stock/', views.admin_stock, name='admin_stock'),
    path('stock/add/', views.stock_add, name='stock_add'),
    path('stock/edit/<int:pk>/', views.stock_edit, name='stock_edit'),
    path('stock/delete/<int:pk>/', views.stock_delete, name='stock_delete'),
    
    
    #URl - отвечающие за отображение акций, редактирование и удаление акций
    path('stock/', views.admin_stock, name='admin_stock'),
    path('stock/add/', views.stock_add, name='stock_add'),
    path('stock/edit/<int:pk>/', views.stock_edit, name='stock_edit'),
    path('stock/delete/<int:pk>/', views.stock_delete, name='stock_delete'),
    
    #URl - отвечающие за отображение Слайдера главной страницы, редактирование и удаление услуг
    path('admin-slider/', views.admin_slider, name='admin_slider'),
    path('admin-slider/add/', views.slider_add, name='slider_add'),
    # path('serv/edit/<int:pk>/', views.service_edit, name='service_edit'),
    # path('serv/delete/<int:pk>/', views.service_delete, name='service_delete'),
    
    #URl - Шаблон главной страницы
    path('home/', views.admin_home, name='admin_home'),
    
    #URl - Шаблон общих настроек сайта
    path('settings/', views.admin_settings, name='admin_settings'),
    path('messanger/', views.admin_messanger, name='messanger'),
    path('messanger/add/', views.messanger_add, name='messanger_add'),
    path('messanger/edit/<int:pk>/', views.messanger_edit, name='messanger_edit'),
    path('messanger/delete/<int:pk>/', views.messanger_delete, name='messanger_delete'),
]