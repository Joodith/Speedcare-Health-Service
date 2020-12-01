from django import template
register=template.Library()
def replace(value):
    value=False

register.filter('replace',replace)