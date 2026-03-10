"""Модуль с настроками url путей для приложения products"""
from django.urls import path

from .views import HelloWorldView


app_name = "products"

urlpatterns = [
    path('', HelloWorldView.as_view(), name="hello"),
]
