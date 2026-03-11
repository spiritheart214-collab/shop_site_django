import csv
from typing import List, Dict, Union

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import URLPattern, URLResolver, path
from django.utils.html import format_html

from .models import Category
from .forms import CSVImportForm
from .services import parse_csv, create_categories


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка админ панели для категорий"""
    actions = ["export_as_csv"]
    change_list_template = "products/products_change_list.html"

    list_display = ["name", "parent", "icon_preview", "is_active", "is_soft_deleted"]
    list_display_links = ["name", "parent", "is_active", "is_soft_deleted"]
    list_filter = ("name", "is_active", "is_soft_deleted")
    search_fields = ["name"]
    readonly_fields = ["icon_preview_large"]
    ordering = ("name", "id")

    # Поля для обновления существующих записей
    fieldsets = (
        (
            "Категория", {
                "fields": ("name", "parent", "icon_preview_large"),
                "classes": ("wide",)
            }),

        (
            "Состояние", {
                "fields": ("is_active", "is_soft_deleted"),
                "classes": ("wide",)
            }),
        (
            "Иконка (загрузить / обновить)", {
                "fields": ("icon",),
                "classes": ("wide", "collapse")
            })
    )

    def icon_preview(self, obj: Category) -> str:
        """Показать иконку товара в админке (список всех товаров)"""

        if obj.icon:
            style_format = ('<img src="{}" style="width:40px; '
                            'height:40px; border-radius:20%; '
                            'object-fit:cover; '
                            'background-color: white;" />')

            html_icon = format_html(
                style_format,
                obj.icon.url
            )
            return html_icon
        return "-"

    icon_preview.short_description = "Иконка"

    def icon_preview_large(self, obj: Category) -> str:
        """Показать иконку товара в админке (конкретная запись)"""
        if obj.icon:
            style_format = ('<img src="{}" style="width:150px; '
                            'height:150px; '
                            'border-radius:10%; '
                            'object-fit:cover; '
                            'background-color: white"/>')

            html_icon = format_html(
                style_format,
                obj.icon.url
            )
            return html_icon
        return "Иконка не загружена"

    icon_preview_large.short_description = "Текущая иконка"

    @admin.action(description="Экспорт в csv")
    def export_as_csv(self, request: HttpRequest, queryset: QuerySet[Category]) -> HttpResponse:
        """Экспорт выбранных категорий в CSV"""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="categories.csv"'

        writer = csv.writer(response)

        # Добавляем BOM (fix для чтения русских символов)
        response.write('\ufeff')

        # Заголовки
        writer.writerow([
            "name",
            "parent",
            "is_active",
            "is_soft_deleted"
        ])

        # Данные
        for category in queryset:
            writer.writerow([
                category.name,
                category.parent.name if category.parent else "",
                category.is_active,
                category.is_soft_deleted
            ])

        return response

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
        result: Dict[str, Union[int, str]] = create_categories(сategories_list=csv_reader)

        # УСПЕХ
        self.message_user(request=request,
                          message=f"Cозданно категорий {result['success']}",
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
            /import_categories_csv/ — страница импорта категорий из CSV.

        Возвращает:
            Список URL-путей, включая стандартные и пользовательские.
        """
        urls = super().get_urls()
        import_csv_url = [path("import_categories_csv/", self.import_csv, name="import_categories_csv")]

        return import_csv_url + urls
