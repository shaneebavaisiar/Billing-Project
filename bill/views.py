from django.shortcuts import render,redirect
from .forms import OrderCreateForm,OrderLineForm,BillSearch,UserRegForm
from django.views.generic import TemplateView
from .models import Order,OrderLines,Product,Purchase
from django.db.models import Sum
from django.contrib.auth import authenticate,login,logout
from .filters import OrderFilter
from bill.decorators import admin_only
from django.utils.decorators import method_decorator
from bill.authentication import EmailAuthBackend

# Create your views here.
# @method_decorator(admin_only,name='dispatch')
class OrderCreateView(TemplateView):
    model=Order
    from_class=OrderCreateForm
    template_name = 'bill/ordercreate.html'
    context={}
    def get(self, request, *args, **kwargs):

        order=self.model.objects.last()
        if order:
            last_billnum=order.bill_number
            print(last_billnum)
            lst=int(last_billnum.split('-')[1])+1
            bill_number='lulu-'+str(lst)
        else:
            bill_number='lulu-1000'

        form = self.from_class(initial={'bill_number':bill_number})
        self.context['form'] = form
        return render(request,self.template_name,self.context)

    def post(self,request,*args,**kwargs):
        form=self.from_class(request.POST)
        if form.is_valid():
            bill_number=form.cleaned_data.get('bill_number')
            form.save()
            return redirect('orderline',bill_num=bill_number)
# @method_decorator(admin_only,name='dispatch')
class OrderLineView(TemplateView):
    model=OrderLines
    from_class=OrderLineForm
    template_name = 'bill/orderline.html'
    context={}
    def get(self, request, *args, **kwargs):
        bill_number=kwargs['bill_num']
        form=self.from_class(initial={'bill_number':bill_number})

        self.context['form']=form
        queryset = self.model.objects.filter(bill_number__bill_number=bill_number)
        self.context['items']=queryset
        total=OrderLines.objects.filter(bill_number__bill_number=bill_number).aggregate(Sum('amount'))
        ctotal=total['amount__sum']
        self.context['total']=ctotal
        self.context['bill_number']=bill_number
        return render(request,self.template_name,self.context)

    def post(self,request,*args,**kwargs):
        form=self.from_class(request.POST)
        if form.is_valid():
            bill_number=form.cleaned_data.get('bill_number')
            bill=Order.objects.get(bill_number=bill_number) # created instance bcz it is forignkey
            product_name=form.cleaned_data.get('product_name')
            prdt=Product.objects.get(product_name=product_name) # create instance  bcz it is forignkey
            qty=form.cleaned_data.get('product_qty')
            product = Purchase.objects.get(product__product_name=product_name)
            amount=product.selling_price*qty
            orderline=self.model(bill_number=bill,product=prdt,product_qty=qty,amount=amount)
            orderline.save()
            print('order saved')
            return redirect('orderline', bill_num=bill_number)

# @method_decorator(admin_only,name='dispatch')
class BillGenerate(TemplateView):
    def get(self, request, *args, **kwargs):
        bill_number=kwargs.get('billnum')
        total = OrderLines.objects.filter(bill_number__bill_number=bill_number).aggregate(Sum('amount'))
        grandtotal = total['amount__sum']
        order=Order.objects.get(bill_number=bill_number)
        order.bill_total=grandtotal
        order.save()
        queryset = OrderLines.objects.filter(bill_number__bill_number=bill_number)
        context={}
        context['items']=queryset
        context['gtotal']=grandtotal
        return render(request,'bill/customerbill.html',context)
# my own code for bill search
class BillSearch(TemplateView):
    form_class=BillSearch
    template_name = 'bill/billsearch.html'
    context={}
    def get(self, request, *args, **kwargs):
        form=self.form_class()
        self.context['form']=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            bill_number=form.cleaned_data.get('bill_number')
            return redirect('finalbill',bill_number)
class FinalBill(TemplateView):
    model=OrderLines
    context={}
    template_name = 'bill/finalbill.html'
    def get(self, request, *args, **kwargs):
        bill_number=kwargs['bill_number']
        items=self.model.objects.all().filter(bill_number__bill_number=bill_number)
        self.context['items']=items
        order=Order.objects.get(bill_number=bill_number)
        # grandtotal=order.bill_total
        self.context['order']=order

        return render(request,self.template_name,self.context)
# end my own code for bill search
# user section
class UserRegistration(TemplateView):
    form_class=UserRegForm
    template_name = 'bill/userreg.html'
    context={}
    def get(self, request, *args, **kwargs):
        form=self.form_class()
        self.context['form']=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userlogin')
        else:
            self.context['form']=self.form_class()
            return render(request, self.template_name, self.context)


class UserLogin(TemplateView):
    template_name = 'bill/login.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
    def post(self,request,*args,**kwargs):
        email=request.POST.get('email')
        password=request.POST.get('pwd')
        obj=EmailAuthBackend()
        user=obj.authenticate(request,username=email,password=password)
        if user:
            login(request,user)
            return render(request,'bill/home.html')
        else:
            return render(request,self.template_name)

class UserLogout(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('userlogin')

# end user section

# inbuilt bill search
class BillSearchInbulit(TemplateView):
    def get(self, request, *args, **kwargs):
        orders=Order.objects.all()
        context={}
        orderfilter=OrderFilter(request.GET,queryset=orders)
        context['filter']=orderfilter
        return render(request,'bill/search.html',context)
# end inbuit bill search