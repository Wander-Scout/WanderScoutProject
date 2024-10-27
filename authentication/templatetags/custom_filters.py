# authentication/templatetags/custom_filters.py
from django import template

register = template.Library() # registers this file with Django's template system for custom filters

@register.filter(name='add_class')
def add_class(field, css): # applies a CSS class to a form field widget dynamically in a template
    return field.as_widget(attrs={"class": css})
