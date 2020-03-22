from django import template

register = template.Library()


@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)


@register.filter
def minus(value):
    return value - 1


@register.filter
def sum(value1, value2):
    return value1 + value2


