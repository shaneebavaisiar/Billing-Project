from django.forms import ModelForm
from django import forms
from .models import Order,Purchase,Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class OrderCreateForm(ModelForm):
    class Meta:
        model=Order
        fields=['bill_number','customer_name','phone_number']


class OrderLineForm(forms.Form):
    bill_number=forms.CharField()
    products=Purchase.objects.all().values_list('product__product_name')
    result=[(itemtuple[0],itemtuple[0]) for itemtuple in products]
    product_name=forms.ChoiceField(choices=result)
    product_qty=forms.IntegerField()

class BillSearch(forms.Form):
    billnum=Order.objects.all().values_list('bill_number')
    choices=[(bill[0],bill[0]) for bill in billnum]
    bill_number=forms.ChoiceField(choices=choices)

class UserRegForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2']