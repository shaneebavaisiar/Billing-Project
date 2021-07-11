from django.contrib import admin

# Register your models here.
from .models import Order,OrderLines,Product,Purchase

admin.site.register(Product)
admin.site.register(Purchase)
