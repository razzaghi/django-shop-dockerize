from django import template
from product.models import Category
from product.views import get_user
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def categories():
    return Category.objects.all()

@register.simple_tag
def is_bought(product, user):
    return product.is_bought(user.id)


@register.simple_tag
def is_ended(product, user):
    return product.is_ended(user.id)


@register.simple_tag
def is_favorite(product, user):
    return product.is_favorite(user.id)


@register.simple_tag
def is_liked(product, user):
    return product.is_liked(user.id)


@register.simple_tag
def is_shared(product, user):
    return product.is_shared(user.id)

@register.simple_tag
def views_count(product, user):
    return product._views_count_add(user)





