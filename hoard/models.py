from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Product(models.Model):
    TYPE = [
            ('Sell','Sell'),
            ('Rent','Rent'),
            ('Sell or Rent','Sell or Rent'),
    ]
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    title       = models.CharField(max_length = 25)
    type        = models.CharField(max_length = 12, choices = TYPE, default = 'Sell')
    price       = models.IntegerField()
    description = models.TextField(default="No Description Given")
    image       = models.ImageField(default='default.jpeg',upload_to='product')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')
