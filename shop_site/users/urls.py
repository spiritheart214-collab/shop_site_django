from django.urls import path

from .views import UserRegistrationView, UserLoginView, UserLogoutView, HelloWorldView


app_name = "users"

urlpatterns = [
    path("", HelloWorldView.as_view(), name="hello_world"),

    path("register/", UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name='login'),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
