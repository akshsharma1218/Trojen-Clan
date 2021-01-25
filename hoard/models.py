from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Owner(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    name        = models.CharField(max_length=60, null=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    TYPE = [
            ('Sell','Sell'),
            ('Rent','Rent'),
            ('Sell or Rent','Sell or Rent'),
    ]
    owner       = models.ForeignKey(Owner, on_delete=models.CASCADE)
    title       = models.CharField(max_length = 25)
    type        = models.CharField(max_length = 12, choices = TYPE, default = 'Sell')
    price       = models.IntegerField()
    description = models.TextField(default="No Description Given")
    image       = models.ImageField(default='default.jpeg', upload_to='media/product')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store')

class Customer(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    name        = models.CharField(max_length=60,null=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    customer        = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered    = models.DateTimeField(default=timezone.now)
    complete        = models.BooleanField(default=False)
    transaction_id  = models.CharField(max_length=100, unique=True)
    products        = models.ManyToManyField(Product)

    def __str__(self):
        return self.customer.user.username

    def cart_items(self):
        return self.products.count

    def get_total(self):
        return sum([product.price for product in self.products.all()])
