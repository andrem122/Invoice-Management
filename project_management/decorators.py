"""Custom Decorators"""
from functools import wraps

#checks if the user is active and a customer or a customer's staff
def customer_and_staff_check(user):
    if user.is_active and user.groups.filter(name__in=['Customers', 'Customers Staff']).exists():
        return True
    else:
        return False

#checks if the user is active and a worker
def worker_check(user):
    if user.is_active and user.groups.filter(name='Workers').exists():
        return True
    else:
        return False

def is_post_method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            attribute = getattr(arg, 'method')
            if attribute == 'POST':
                return func(*args, **kwargs)

        for kwarg in kwargs.values():
            attribute = getattr(kwarg, 'method')
            if attribute == 'POST':
                return func(*args, **kwargs)

        return False

    return wrapper

if __name__ == '__main__':
    customers_and_staff()
    worker_check()
