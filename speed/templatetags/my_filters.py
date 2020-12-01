from django import template
register=template.Library()
def add(value,arg):
    return value.replace(arg,'')
register.filter('add',add)