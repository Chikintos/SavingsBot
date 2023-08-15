
from django.contrib import admin
from django.urls import path,include
from .views import base_view


urlpatterns = [
    path('', base_view),
]