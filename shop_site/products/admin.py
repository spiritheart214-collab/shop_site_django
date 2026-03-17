import csv
from typing import List, Dict, Union

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import URLPattern, URLResolver, path
from django.utils.html import format_html

from .models import Category, Product
from .forms import CSVImportForm
from .services import parse_csv, create_categories, create_products


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка админ панели для категорий"""
    actions = ["export_as_csv"]
    change_list_template = "products/category_change_list.html"

    list_display = ["name", "parent", "icon_preview", "is_active", "is_soft_deleted", "formatted_created_at"]
    list_display_links = ["name", "parent", "is_active", "is_soft_deleted"]
    list_filter = ("name", "is_active", "is_soft_deleted")
    search_fields = ["name"]
    readonly_fields = ["icon_preview_large"]
    ordering = ("name",)

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

    def formatted_created_at(self, obj: Category) -> str:
        """Возвращает отформатированную дату создания"""
        return obj.created_at.strftime("%d.%m.%Y")

    formatted_created_at.short_description = "Дата создания"
    formatted_created_at.admin_order_field = "created_at"

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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка админ панели для продуктов"""

    actions = ["export_as_csv"]
    change_list_template = "products/product_change_list.html"

    list_display = ["manufacturer", "name", "short_description", "price", "product_preview", "formatted_updated_at"]
    list_display_links = ["name", "manufacturer", ]
    list_filter = ("name", "created_at", "updated_at", "is_soft_deleted", "is_limited_edition", "price")
    readonly_fields = ["product_preview_large", "formatted_created_at", "formatted_updated_at"]
    search_fields = ["manufacturer", "name"]
    ordering = ("manufacturer", "name", "updated_at")

    # Поля для обновления существующих записей
    fieldsets = (
        (
            "Продукт", {
                "fields": ("category", "manufacturer", "name", "product_preview_large", "description", "price"),
                "classes": ("wide",)
            }),

        (
            "Состояние", {
                "fields": ("is_limited_edition", "is_soft_deleted", "sort_index"),
                "classes": ("wide", "collapse")
            }),

        (
            "Cоздан/Обновлен", {
                "fields": ("formatted_created_at", "formatted_updated_at"),
                "classes": ("wide", "collapse")
            }),

        (
            "Иконка (загрузить / обновить)", {
                "fields": ("image",),
                "classes": ("wide", "collapse")
            })
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Оптимизация запросов с подгрузкой связанных категорий"""
        return super().get_queryset(request).select_related("category")

    def short_description(self, model: Product) -> str:
        """Корокое описание продукта"""
        """Возвращает короткое описание продукта"""
        if model.description and len(model.description) > 100:
            return model.description[:50] + "..."
        return model.description

    short_description.short_description = "Описание"

    def formatted_created_at(self, obj: Product) -> str:
        """Возвращает отформатированную дату создания"""
        return obj.created_at.strftime("%d.%m.%Y")

    formatted_created_at.short_description = "Cоздан"
    formatted_created_at.admin_order_field = "created_at"

    def formatted_updated_at(self, obj: Product) -> str:
        """Возвращает отформатированную дату обновления"""
        return obj.updated_at.strftime("%d.%m.%Y")

    formatted_updated_at.short_description = "Обновлен"
    formatted_updated_at.admin_order_field = "updated_at"

    def product_preview(self, obj: Product) -> str:
        """Показать товар в админке (список всех товаров)"""

        if obj.image:
            style_format = ('<img src="{}" style="width:40px; '
                            'height:40px; border-radius:20%; '
                            'object-fit:cover; '
                            'background-color: white;" />')

            html_img = format_html(
                style_format,
                obj.image.url
            )
            return html_img
        return "-"

    product_preview.short_description = "Фото"

    def product_preview_large(self, obj: Product) -> str:
        """Показать товар в админке (конкретная запись)"""
        if obj.image:
            style_format = ('<img src="{}" style="width:150px; '
                            'height:150px; '
                            'border-radius:10%; '
                            'object-fit:cover; '
                            'background-color: white"/>')

            html_icon = format_html(
                style_format,
                obj.image.url
            )
            return html_icon
        return "Фото продукта не загружено"

    product_preview_large.short_description = "Текущие фото"

    @admin.action(description="Экспорт товаров в csv")
    def export_as_csv(self, request: HttpRequest, queryset: QuerySet[Product]) -> HttpResponse:
        """Экспорт выбранных товаров в CSV"""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="products.csv"'

        writer = csv.writer(response)

        # Добавляем BOM (fix для чтения русских символов)
        response.write('\ufeff')

        # Заголовки
        writer.writerow([
            "name",
            "manufacturer",
            "category",
            "price",
            "description",
            "sort_index",
            "is_limited_edition",
            "is_soft_deleted",
            "created_at",
            "updated_at"
        ])

        # Данные
        for product in queryset:
            writer.writerow([
                product.name,
                product.manufacturer,
                product.category.name if product.category else "",
                str(product.price),
                product.description[:100] + "..." if len(product.description) > 100 else product.description,
                product.sort_index,
                product.is_limited_edition,
                product.is_soft_deleted,
                product.created_at.strftime("%d.%m.%Y"),
                product.updated_at.strftime("%d.%m.%Y")
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

        result: Dict[str, Union[int, str]] = create_products(products_list=csv_reader)

        # УСПЕХ
        self.message_user(request=request,
                          message=f"Cозданно продуктов {result['success']}",
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
        import_csv_url = [path("import_products_csv/", self.import_csv, name="import_products_csv")]

        return import_csv_url + urls


# Todo на всех страницах пишется Импорт пользовталей