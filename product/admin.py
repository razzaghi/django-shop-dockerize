from django.contrib import admin
# Register your models here.
from django.contrib.admin import ModelAdmin

from product import models

@admin.register(models.Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "price", "category", "discount_percent", "rate", "review_count",)


@admin.register(models.ActionsLog)
class ProductAdmin(ModelAdmin):
    list_display = ("create_date","user","product","session_key","ip","action","value")

@admin.register(models.Category)
class ProductAdmin(ModelAdmin):
    list_display = ("name",)



