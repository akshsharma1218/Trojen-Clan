from django.shortcuts import render, redirect
from django.contrib import messages
from .admin import UserCreationForm
from .models import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.views.generic import (
    UpdateView,
    DeleteView,
    CreateView,
    DetailView,
)

def index(request):
    products = Product.objects.filter(is_available=True).order_by('-id')[:4]
    context =  {'products':products,'top':'-top','header':'header-transparent'}
    return render(request, 'hoard/index.html', context)

def checkout(request):
    try:
        order = Order.objects.get(customer=request.user,complete=False)
        for product in order.products.all():
            if product.is_available == 'False':
                order.products.remove(product)
        context =  {'cust':'cust','cartItems': order.cart_items()}
    except ObjectDoesNotExist:
        order = None
        context =  {'cust':'cust','cartItems':0}
    return render(request, 'hoard/checkout.html', context)

def store(request):
    products = Product.objects.filter(~Q(owner = request.user),is_available=True)
    try:
        order = Order.objects.get(customer=request.user,complete=False)
        for product in order.products.all():
            if product.is_available == False:
                order.products.remove(product)
        context =  {'products':products,'cust':'cust','cartItems': order.cart_items()}
    except ObjectDoesNotExist:
        order = None
        context =  {'products':products,'cust':'cust','cartItems':0}
    return render(request, 'hoard/store.html', context)

def cart(request):
    if  request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user,complete=False)
        for product in order.products.all():
            if product.is_available == False:
                order.products.remove(product)
        context = {'order': order,'total':order.get_total(),'cust':'cust', 'cartItems': order.cart_items()}
        return render(request, 'hoard/cart.html',context)
    else:
        return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            uservalue = form.cleaned_data.get('username')
            messages.success(request,f'Account Created for {uservalue}')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'hoard/register.html', {'form':form})

class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        try:
            order = Order.objects.get(customer=self.request.user, complete=False)
            context.update({'cust':'cust','cartItems':order.cart_items()})
        except ObjectDoesNotExist:
            context.update({'cust':'cust','cartItems':'x'})
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title','type','category','sub','price','description', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title','type', 'price','description', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.owner:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.owner:
            return True
        return False

def updateItem(request):
    productID = request.POST.get('productID')
    action = request.POST.get('action')
    customer = request.user
    print(action)
    print(productID)
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete = False)

    if action=='add':
        order.products.add(product)
    elif action=='remove':
        order.products.remove(product)
    order.save()

    if not order.products:
        order.delete()

    context={'cartItems': order.cart_items(),'order':order}
    if request.is_ajax:
        cart_html= render_to_string('hoard/cart_product.html', context , request=request)
        html= render_to_string('hoard/cart_var.html', context , request=request)
        context = { 'form': html, 'cart':cart_html }
        return JsonResponse(context)
