from django import template

register = template.Library()


@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)


@register.filter
def seconds(time):
    return (time.hour * 3600) + (time.minute * 60) + time.second



