
from django.contrib import admin
from django.urls import path
from video import views

urlpatterns = [
    path('index', views.index, name='home'),
]
