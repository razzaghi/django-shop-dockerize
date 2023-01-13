from django import template
from product.models import Category

register = template.Library()

@register.simple_tag
def categories():
    return Category.objects.all()

@register.simple_tag
def is_bought(product, request):
    return product.is_bought(request)


@register.simple_tag
def is_ended(product, request):
    return product.is_ended(request)


@register.simple_tag
def is_favorite(product, request):
    return product.is_favorite(request)


@register.simple_tag
def is_liked(product, request):
    return product.is_liked(request)


@register.simple_tag
def is_shared(product, request):
    return product.is_shared(request)

@register.simple_tag
def views_count(product, request):
    return product._views_count_add(request)





