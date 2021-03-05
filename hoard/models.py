from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import RegexValidator


class User(AbstractUser):
    name      = models.CharField(max_length=20)
    phone_reg = RegexValidator(regex=r'^\+?9?1?\d{9,10}$', message="Phone number must be entered in the format: '+91XXXXXXXXXX'.")
    phone_num = models.CharField(validators=[phone_reg], max_length=13, blank=True) # validators should be a list
    email     = models.EmailField()
    address   = models.CharField(max_length = 50)
    credits   = models.IntegerField(null=True)
    coupan    = models.CharField(max_length=6)

    def __str__(self):
        return self.username

class Product(models.Model):
    TYPE = [
            ('Sell','Sell'),
            ('Rent','Rent'),
            ('Sell or Rent','Sell or Rent'),
    ]
    Category = [
            ('Gate','Gate'),
            ('Novel','Novel'),
            ('1st year','1st year'),
            ('2nd year','2nd year'),
            ('3rd year','3rd year'),
            ('4th year','4th year'),
            ('5th year','5th year'),
            ('All','Other'),
    ]
    Subject = [
            ('Math','Math'),
            ('Physics','Physics'),
            ('Chemistry ','Chemistry '),
            ('C ','C '),
            ('Engineering','Engineering'),
            ('All','Other'),
    ]
    owner        =  models.ForeignKey(User, on_delete=models.CASCADE)
    title        =  models.CharField(max_length = 25)
    type         =  models.CharField(max_length = 12, choices = TYPE, default = 'Sell')
    category     =  models.CharField(max_length = 12, choices = Category, default = 'Gate')
    sub          =  models.CharField(max_length = 12, choices = Subject, default = 'Math')
    price        =  models.IntegerField()
    description  =  models.TextField(default="No Description Given")
    image        =  models.ImageField(default='default.jpeg', upload_to='product')
    is_available =  models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store')


class Order(models.Model):
    customer        = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered    = models.DateTimeField(null=True,blank=True)
    has_done        = models.BooleanField(default=False)
    complete        = models.BooleanField(default=False)
    amount_paid     = models.BooleanField(default=False)
    transaction_id  = models.CharField(max_length=100, unique=True, null=True)
    products        = models.ManyToManyField(Product)

    def __str__(self):
        return self.customer.username

    def cart_items(self):
        return self.products.count

    def get_total(self):
        return sum([product.price for product in self.products.all()])
