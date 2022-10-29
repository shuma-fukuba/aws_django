from django.db import models

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=32)
    amount = models.IntegerField()
    price = models.IntegerField()
