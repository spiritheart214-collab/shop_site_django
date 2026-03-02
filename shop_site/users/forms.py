from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

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


class UserUpdatePasswordForm(PasswordChangeForm):
    """Форма обновления пароля пользователя"""

    def __init__(self, *args, **kwargs):
        """Добавление класса и placeholder к стандартному PasswordChangeForm"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Введите {field.label.lower()}'
            })


class CSVImportForm(forms.Form):
    """Форма для ипорта CSV в админ панели"""
    csv_file: forms.FileField = forms.FileField(
        label="CSV файл",
        help_text="Загрузите CSV файл с пользователями"
    )

    def clean_csv_file(self):
        """
        Валидация импортируемого файла
        - Нельзя загрузить никакие форматы кроме CSV
        - Нельзя загрузить больше 5mb
        """
        csv_file = self.cleaned_data["csv_file"]

        if not csv_file.name.endswith(".csv"):
            raise forms.ValidationError("Файл должен быть в формате CSV")

        if csv_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Файл слишком большой (макс 5MB)")

        return csv_file


class CustomUserCreationForm(CleanDataMixin, UserCreationForm):
    """Форма создания пользователя (через админ панель)"""
    class Meta:
        """Настройка формы"""
        model = User
        fields = ("username", "first_name", "last_name", "patronymic", "email", "telephone", "avatar")
