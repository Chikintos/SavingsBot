from django.shortcuts import render
# Create your views here.
from .models import *
from django.http import HttpResponse


def base_view(request):
    return HttpResponse("<h2><a href='/admin'>Admin panel</a></h2><br><h3>Login: admin<br>Password: admin</h3>")