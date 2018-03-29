"""Custom Decorators"""
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

if __name__ == '__main__':
    customers_and_staff()
    worker_check()
