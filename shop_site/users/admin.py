from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Настройка админ панели для пользователя"""

    list_display = ["colored_full_name", "email_link", "telephone", "avatar_prewiew"]
    list_display_links = ["colored_full_name", "telephone"]
    list_filter = ("first_name", "date_joined",)
    search_fields = ["first_name", "last_name", "email", "telephone"]
    readonly_fields = ["avatar_prewiew_large"]
    ordering = "-date_joined",

    fieldsets = (
        (
            "Личные данные", {
                "fields": ("first_name", "last_name", "patronymic", "email", "telephone",
                           "avatar_prewiew_large", "avatar"),
                "classes": ("wide",)
            }),

        (
            "Системные данные", {
                "fields": ("password", "last_login", "date_joined"),
                "classes": ("wide", "collapse")
            })
    )

    def avatar_prewiew(self, obj: User) -> str:
        """Показать аватар пользователя в админке (список всех пользователей)"""

        if obj.avatar:
            html_avatar = format_html(
                '<img src="{}" style="width:40px; height:40px; border-radius:30%; object-fit:cover;" />',
                obj.avatar.url
            )
            return html_avatar
        return "-"
    avatar_prewiew.short_description = "Аватар"

    def avatar_prewiew_large(self, obj: User) -> str:
        """Показать аватар пользователя в админке (конкретная запись)"""
        if obj.avatar:
            html_avatar = format_html(
                '<img src="{}" style="width:150px; height:150px; border-radius:10%; object-fit:cover;" />',
                obj.avatar.url
            )
            return html_avatar
        return "Фото не загруженно"
    avatar_prewiew_large.short_description = "Текущий аватар"

    def colored_full_name(self, obj: User) -> str:
        """Подсветка текста для суперпользователя и администратора"""

        # Суперпользователь
        if obj.is_superuser:
            html_superuser = format_html(
                '<span style="color: #d8eb34; font-weight: bold;">{}</span>',
                obj.full_name
            )
            return html_superuser

        # Администратор
        elif obj.is_staff:
            html_staff = format_html(
                '<span style="color: #32a852; font-weight: bold;">{}</span>',
                obj.full_name
            )
            return html_staff

        return obj.full_name
    colored_full_name.short_description = "ФИО"

    def email_link(self, obj: User) -> str:
        """Кликабельная почта"""
        email = format_html(
            '<a href="mailto:{}">{}</a>',
            obj.email,
            obj.email
        )

        return email
    email_link.short_description = "Email"
