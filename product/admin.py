from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from product import models


@admin.register(models.Product)
class ProductAdmin(ModelAdmin):
    pass

@admin.register(models.Category)
class ProductAdmin(ModelAdmin):
    pass