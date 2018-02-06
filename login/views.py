from django.http import HttpResponse

def index(request):
    return HttpResponse('<h1>Login Page</h1>')
