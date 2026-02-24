from django.urls import path

from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserDetailView, UserUpdateView


app_name = "users"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name='login'),
    path("logout/", UserLogoutView.as_view(), name="logout"),

    path("user/<int:pk>/", UserDetailView.as_view(), name="user"),
    path("user/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
]
