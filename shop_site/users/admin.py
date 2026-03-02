import csv
from typing import List, Dict, Union

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path, URLPattern, URLResolver
from django.utils.html import format_html

from .forms import CSVImportForm, CustomUserCreationForm
from .models import User
from .services import create_users, parse_csv


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Настройка админ панели для пользователя"""
    actions = ["export_as_csv"]

    add_form = CustomUserCreationForm
    change_list_template = "users/user_changelist.html"

    list_display = ["colored_full_name", "email_link", "telephone", "avatar_prewiew"]
    list_display_links = ["colored_full_name", "telephone"]
    list_filter = ("first_name", "date_joined",)
    search_fields = ["first_name", "last_name", "email", "telephone"]
    readonly_fields = ["avatar_prewiew_large"]
    ordering = "-date_joined",

    # Поля для 'Создать нового пользователя' в админ панели
    add_fieldsets = (
        ("Логин - пороль", {
            "fields": ("username", "password1", "password2"),
            "classes": ("wide",),
        }),

        (
            "Данные пользователя", {
                "fields": ("first_name", "last_name", "patronymic", "email", "telephone", "avatar"),
                "classes": ("wide",)
            })
    )

    # Поля для обновления существующих записей
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

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        """Отображает страницу в админке для импорта пользователей из CSV файла."""
        # GET
        if request.method == "GET":
            form = CSVImportForm()
            context = {"form": form}

            return render(request=request, template_name="admin/csv_form.html", context=context)

        # POST
        form = CSVImportForm(request.POST, request.FILES)

        # POST INVALID
        if not form.is_valid():
            context = {"form": form}
            return render(request=request, template_name="admin/csv_form.html", context=context, status=400)

        # POST VALID
        byte_file = form.files["csv_file"].file

        csv_reader: List[Dict[str, str]] = parse_csv(uploaded_file=byte_file)
        result: Dict[str, Union[int, str]] = create_users(users_list=csv_reader)

        # УСПЕХ
        self.message_user(request=request,
                          message=f"Cозданно пользователей {result["success"]}",
                          level=messages.SUCCESS)
        # ОШИБКИ
        if result["errors"]:
            for error in result["errors"]:
                self.message_user(request=request, message=error, level=messages.ERROR)

        return redirect("..")

    def get_urls(self) -> List[URLPattern | URLResolver]:
        """
        Расширяет стандартные URL-адреса админки.

        Добавляет кастомный маршрут:
            /import_user_csv/ — страница импорта пользователей из CSV.

        Возвращает:
            Список URL-путей, включая стандартные и пользовательские.
        """
        urls = super().get_urls()
        import_csv_url = [path("import_user_csv/", self.import_csv, name="import_user_csv")]

        return import_csv_url + urls

    @admin.action(description="Экспорт в csv")
    def export_as_csv(self, request: HttpRequest, queryset: QuerySet[User]) -> HttpResponse:
        """Экспорт выбранных пользователей в CSV"""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)

        # Добавляем BOM (fix для чтения русских символов)
        response.write('\ufeff')

        # Заголовки
        writer.writerow([
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "telephone",
            "date_joined",
        ])

        # Данные
        for user in queryset:
            writer.writerow([
                user.id,
                user.username,
                user.first_name,
                user.last_name,
                user.email,
                user.telephone,
                user.date_joined,
            ])

        return response
