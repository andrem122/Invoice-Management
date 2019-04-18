from django import template

register = template.Library()

def next_item(iterable):
    """Returns next item in an iterable"""
    return next(iterable)

def add_dashes(string):
    return string.replace(' ', '-')

register.filter('next_item', next_item)
register.filter('add_dashes', add_dashes)
