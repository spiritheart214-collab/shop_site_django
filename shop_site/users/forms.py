from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.files.uploadedfile import InMemoryUploadedFile

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


class UserUpdateForm(forms.ModelForm):
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
                return forms.ValidationError(f"'Размер фото не должен превышать {size_limit} МБ'")

            return avatar

    def clean_email(self):
        """Валидация еmail. Ошибка, если такой email уже есть"""
        email = self.cleaned_data.get("email")
        is_email_exists = User.objects.exclude(pk=self.instance.pk).filter(email=email).exists()

        if is_email_exists:
            raise forms.ValidationError(f"Пользователь с таким email ({email}) уже существует")
        return email

    def clean_telephone(self):
        """Валидация телефона. Ошибка, если такой телефон уже есть"""
        telephone = self.cleaned_data.get('telephone')
        is_telephone_exist = User.objects.exclude(pk=self.instance.pk).filter(telephonel=telephone).exists()

        if is_telephone_exist:
            raise forms.ValidationError(f"Пользователь с таким телефоном ({telephone}) уже существует")
        return telephone

# Todo - сделать валидаторы на каждое поле. Определить их в миксин и подмешать к двум формам
# Todo - должно получиться два миксина form_mixins view_mixin
