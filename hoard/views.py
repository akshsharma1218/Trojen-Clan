from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .admin import UserCreationForm
from .models import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView,
    DetailView,
)
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def index(request):
    products = Product.objects.filter(is_available=True).order_by('-id')[:4]
    context =  {'products':products,'top':'-top','header':'header-transparent'}
    return render(request, 'hoard/index.html', context)

@login_required
def checkout(request):
    if request.method == 'POST':
        user = request.user
        email = user.email
        send_mail(
            'Order Succesful',
            'Your order has been sent.',
            'bookhoardnith@gmail.com',
            [email],
            fail_silently=False,
        )
        order = Order.objects.get(customer=request.user,complete=False)
        owners = list(order.products.all().values_list('owner__email'))
        email_list = [x[0] for x in owners]
        send_mail(
            'Order Received',
            f"""An order has been received from
             Name : {user.email}
             Roll no. : {user.username}
             Phone no. : {user.phone_num},
             Email Id. : {user.email},
             """,
            'bookhoardnith@gmail.com',
            email_list,
            fail_silently=False,
        )
        order.date_ordered = timezone.now()
        order.complete = True
        order.transaction_id = str(order.customer) + str(order.date_ordered) +str(order.id)
        order.save()
        messages.success(request,f'Order completed')
        return redirect('home')
    else:
        user = request.user
        try:
            order = Order.objects.get(customer=request.user,complete=False)
            for product in order.products.all():
                if product.is_available == 'False':
                    order.products.remove(product)
            
            own = order.products.all().values_list('owner')
            owners = [User.objects.get(id=x[0]) for x in own]
            print(owners)
            context =  {'cust':'cust','total':order.get_total(),'user':user,'cartItems': order.cart_items(),'owners':owners}
        except ObjectDoesNotExist:
            order = None
            context =  {'cust':'cust','user':user,'cartItems':0}
    return render(request, 'hoard/checkout.html', context)

@login_required
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

def explore(request):
    return redirect('https://nith.ac.in/research-publications')

def cart(request):
    if  request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
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
            email = form.cleaned_data.get('email')
            send_mail(
                'Account registered on bookhoardnith',
                'Your account has been registered on bookhoard.\nFor any queries contact bookhoardnith@gmail.com',
                'bookhoardnith@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'hoard/register.html', {'form':form})

# @login_required
# def Profile(request):


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=self.request.user, complete=False)
            context.update({'cust':'cust','cartItems':order.cart_items()})
        else:
            context.update({'cust':'cust','cartItems':0})
        return context

class UserProductListView(ListView):
    model = Product
    template_name = 'hoard/user_products.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'products'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Product.objects.filter(owner=user).order_by('-id')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context.update({'name':user.name})
        print(user.name)
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

from django.shortcuts import HttpResponse


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

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

    context={'cartItems': order.cart_items(),'order':order, 'total':order.get_total()}
    if is_ajax(request=request):
        cart_html= render_to_string('hoard/cart_product.html', context , request=request)
        html= render_to_string('hoard/cart_var.html', context , request=request)
        context = { 'form': html, 'cart':cart_html }
        return JsonResponse(context)
