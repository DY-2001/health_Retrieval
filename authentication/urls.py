from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('searching', views.searching, name="searching"),
    path('relevent', views.relevent, name="relevent"),
]