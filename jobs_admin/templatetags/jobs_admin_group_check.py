from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='in_group')
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name)
    return group in user.groups.all()

def add_dashes(string):
    return string.replace(' ', '-')
    
register.filter('add_dashes', add_dashes)
