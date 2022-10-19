from enum import unique
from django.db import models

# Create your models here.
class LongToShort(models.Model):
    long_url=models.URLField(max_length=500)
    short_url=models.CharField(max_length=100, unique=True)
    date=models.DateField(auto_now_add=True)
    clicks=models.IntegerField(default=0)
    
class Meta_Data(models.Model):
    new_short_url=models.CharField(max_length=100,unique=False)
    country_name=models.CharField(max_length=500)
    device_name=models.CharField(max_length=500)
    browser_name=models.CharField(max_length=500)
    last_visit=models.DateTimeField(auto_now_add=True)
    