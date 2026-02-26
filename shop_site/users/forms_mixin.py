"""Миксины форм"""
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UniqueEmailMixin:
    """Миксин для проверки уникальности email"""

    def clean_email(self):
        """Валидация еmail. Ошибка, если такой email уже есть"""
        email = self.cleaned_data.get("email")
        is_email_exists = User.objects.exclude(pk=self.instance.pk).filter(email=email).exists()

        if is_email_exists:
            raise forms.ValidationError(f"Пользователь с таким email ({email}) уже существует")
        return email


class UniqueTelephoneMixin:
    """Миксин для проверки уникальности телефона"""

    def clean_telephone(self):
        """Валидация телефона. Ошибка, если такой телефон уже есть"""
        telephone = self.cleaned_data.get('telephone')
        is_telephone_exist = User.objects.exclude(pk=self.instance.pk).filter(telephone=telephone).exists()

        if is_telephone_exist:
            raise forms.ValidationError(f"Пользователь с таким телефоном ({telephone}) уже существует")
        return telephone


class CleanDataMixin(UniqueEmailMixin, UniqueTelephoneMixin):
    """Общий миксин для валидации данных пользователя"""
    pass