import django_filters
from .models import Customer, Product, Order

class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    # Challenge: created_at range filter
    created_at = django_filters.DateFromToRangeFilter()
    # Challenge: phone pattern (e.g. starts with)
    phone_pattern = django_filters.CharFilter(field_name='phone', lookup_expr='startswith')

    class Meta:
        model = Customer
        fields = ['name', 'email', 'created_at']

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.RangeFilter() # handles gte/lte if range is used or we can field specific
    # Instructions: price__gte, price__lte. RangeFilter usually takes min,max.
    # To strictly follow instructions allow individual args:
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    stock_gte = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock_lte = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']

class OrderFilter(django_filters.FilterSet):
    total_amount_gte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount_lte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    order_date = django_filters.DateFromToRangeFilter()
    
    # Filter by customer name and product name
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    product_name = django_filters.CharFilter(field_name='products__name', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ['total_amount', 'order_date']
