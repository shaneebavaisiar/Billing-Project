"""BillingProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import OrderCreateView,OrderLineView,BillGenerate,BillSearch,\
    FinalBill,UserLogin,UserLogout,UserRegistration,BillSearchInbulit
from django.shortcuts import render
urlpatterns = [
    path('',lambda request:render(request,'bill/base.html')),
    path('admin/', admin.site.urls),
    path('createorder',OrderCreateView.as_view(),name='createorder'),
    path('orderline/<str:bill_num>',OrderLineView.as_view(),name='orderline'),
    path('generatebill/<str:billnum>',BillGenerate.as_view(),name='completeorder'),
    path('billsearch',BillSearch.as_view(),name='billsearch'),
    path('finalbill/<str:bill_number>',FinalBill.as_view(),name='finalbill'),
    path('userregistration', UserRegistration.as_view(), name='register'),
    path('userlogin', UserLogin.as_view(), name='userlogin'),
    path('userlogout', UserLogout.as_view(), name='userlogout'),
    path('search',BillSearchInbulit.as_view(),name='search'),
    path('errorpage',lambda request:render(request,'bill/errorpage.html'),name='errorpage')
]
