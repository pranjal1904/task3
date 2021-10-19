from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_customer = models.BooleanField('Is customer', default=False)
    is_employee = models.BooleanField('Is employee', default=False)
    image = models.ImageField(null=True,blank=True,upload_to="profileimage")


class blog(models.Model):
    title=models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    image = models.ImageField(null=True,blank=True,upload_to="blogimage")
    docid = models.IntegerField(default=0)
    def __str__(self):
        return self.title