from django.contrib import admin

from . import models

admin.site.register(models.Stock)
admin.site.register(models.StockAddition)
admin.site.register(models.StockExpiry)
admin.site.register(models.StockRemoval)
