from django.contrib import admin

from shop.models import Category, Product, Day

# admin.site.register(Categories)
@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}
  
@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}



