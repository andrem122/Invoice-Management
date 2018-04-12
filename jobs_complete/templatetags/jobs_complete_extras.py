from django import template

register = template.Library()

def next_item(iterable):
    """Returns next item in an iterable"""
    return next(iterable)

register.filter('next_item', next_item)
