from pyexpat import model
from django.db import models

# Create your models here.
class ShortLongUrlStore(models.Model):
    long_url = models.URLField(max_length= 500)
    short_url= models.CharField(max_length=10,unique= True)
    date = models.DateTimeField(auto_now_add=True) #this will automatically add the date and time on which a particular row was created
    clicks=models.IntegerField(default= 0)
    username=models.CharField(max_length=30)
