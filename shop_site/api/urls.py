"""Модуль с настроками url путей для приложения"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet


app_name = "api"

routers = DefaultRouter()
routers.register("users_api", UsersViewSet)

urlpatterns = [
    path("users/", include(routers.urls)),
]
