from django.contrib import admin

from bugtracker_app.models import MyDev, Bug

# Register your models here.

admin.site.register(MyDev)
admin.site.register(Bug)
