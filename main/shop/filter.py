import django_filters
from shop import Product

class FlowerFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', lookup_expr='exact')
    color = django_filters.CharFilter(field_name='color', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['category']