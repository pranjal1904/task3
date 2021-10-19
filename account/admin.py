from django.contrib import admin
from .models import User
from account.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(blog)