from django.shortcuts import render, redirect
from django.http import request


def index(request):
    context = {}
    return render(request, "index.html", context)

def bad_request(request, exception, template_name="errors/400.html"):
    return render(request, template_name)

def permission_denied(request, exception, template_name="errors/403.html"):
    return render(request, template_name)

def page_not_found(request, exception, template_name="errors/404.html"):
    return render(request, template_name)
 
def server_error(request, template_name="errors/500.html"):
    return render(request, template_name)
