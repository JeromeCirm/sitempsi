from django import template

register=template.Library()

@register.filter
def tempchr(valeur,base):
    return chr(valeur+base)