from django.contrib import admin 
from . models import Notification, Profile
# Register your models here.
admin.site.register(Profile)
admin.site.register(Notification)