from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    UpdateView,
    DeleteView,
    CreateView,
    DetailView,
)

def index(request):
    products = Product.objects.order_by('-id')[:4]
    context =  {'products':products,'active': 'active','top':'-top', 'header':'header-transparent'}
    return render(request, 'hoard/index.html', context)

def store(request):
    products = Product.objects.all()
    context =  {'products':products}
    return render(request, 'hoard/store.html', context)

def cart(request):
    return render(request, 'hoard/cart.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            uservalue = form.cleaned_data.get('username')
            messages.success(request,'Account Created')
            return redirect('home')
        else:
            messages.warning(request,'ERROR !')
    else:
        form = UserRegisterForm()
    return render(request, 'hoard/register.html', {'form':form})

class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'type', 'price', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['type', 'price']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.user:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.user:
            return True
        return False
