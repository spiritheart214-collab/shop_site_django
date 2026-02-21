from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserRegistrationsForm(UserCreationForm):
    """Форма регистрации пользователя"""

    class Meta:
        """Настройка формы"""
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "telephone",
            "password1",
            "password2"
        )
