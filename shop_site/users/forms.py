from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.files.uploadedfile import InMemoryUploadedFile

from .forms_mixin import CleanDataMixin

User = get_user_model()


class UserRegistrationsForm(CleanDataMixin, UserCreationForm):
    """Форма регистрации пользователя"""

    class Meta:
        """Настройка формы"""
        model = User
        fields = ("username", "email", "telephone", "password1", "password2")

    def clean_username(self):
        """Валидация имени"""
        username: str = self.cleaned_data.get("username")

        if not username:
            raise forms.ValidationError("Введите username")

        if len(username) < 3:
            raise forms.ValidationError("Минимум 3 символа")

        return username


class UserUpdateForm(CleanDataMixin, forms.ModelForm):
    """Форма обновления пользователя"""

    class Meta:
        """Настройка формы"""
        model = User
        fields = ("first_name", "last_name", "patronymic", "email", "telephone", "avatar")

    def clean_avatar(self):
        """Ограничение автара по размеру загрузки"""
        avatar: InMemoryUploadedFile = self.cleaned_data.get("avatar")
        size_limit = 2 * 1024 * 1024

        if avatar:
            if avatar.size > size_limit:
                raise forms.ValidationError(f"'Размер фото не должен превышать {size_limit} МБ'")

            return avatar


class UserUpdatePasswordForm(PasswordChangeForm):
    """Форма обновления пароля пользователя"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Введите {field.label.lower()}'
            })
