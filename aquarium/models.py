

# Create your models here.
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()  # Paise (29900 = ₹299)
    image = models.CharField(max_length=200, blank=True)
    stock = models.IntegerField(default=10)

    def __str__(self):
        return self.name
