from django.contrib import admin

from .models import Sale, Stock

# Register your models here.
admin.site.register(Stock)
admin.site.register(Sale)
