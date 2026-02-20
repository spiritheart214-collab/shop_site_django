from django.urls import path

from .views import UserLoginView, UserLogoutView, HelloWorldView


app_name = "users"

urlpatterns = [
    path("", HelloWorldView.as_view(), name="hello_world"),

    path('login/',UserLoginView.as_view(), name='login'),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
