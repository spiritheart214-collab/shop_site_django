from django.contrib.auth.views import LoginView
from django.urls import path

from .views import HelloWorldView


app_name = "users"

urlpatterns = [
    path("", HelloWorldView.as_view(), name="hello_world"),

    path('login/', LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True,
        next_page='users:hello_world'
    ), name='login'),

]
