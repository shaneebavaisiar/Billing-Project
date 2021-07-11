from bill.models import Order
import django_filters
class OrderFilter(django_filters.FilterSet):
    class Meta:
        model=Order
        fields=['bill_number','customer_name','bill_date']