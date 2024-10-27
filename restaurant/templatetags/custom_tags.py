from django import template

register = template.Library() # set up a template library instance so custom filters can be registered

@register.filter
def is_admin(user):
    return user.groups.filter(name="admin").exists() # check if the user is part of the 'admin' group
