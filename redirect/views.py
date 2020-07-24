from django.shortcuts import redirect

def redirect_login(request):
    """Redirects a user after logging in"""
    if request.user.groups.filter(name='Customers').exists(): #if the user is a customer
        return redirect('/appointments')
    elif request.user.is_superuser:
        return redirect('/admin')
