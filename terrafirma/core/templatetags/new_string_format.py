from django import template

register = template.Library()


@register.filter
def newstrfmt(value, format):
    return format.format(value)
