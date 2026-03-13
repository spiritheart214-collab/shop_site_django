from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError


from .utils import category_icon_path, product_image_path


class Category(models.Model):
    """Модель категорий товаров"""

    class Meta:
        """Настройка отображения в админке."""
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name", "-created_at"]

    name = models.CharField(max_length=255,
                            blank=False,
                            null=False,
                            db_index=True,
                            verbose_name="Категория",
                            help_text="Название категории",

                            error_messages={
                                "max_length": "Название не может быть больше 255 символов",
                                "blank": "Поле не может быть пустым",
                            })

    parent = models.ForeignKey(to="self",
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name="children",
                               verbose_name="Родительская категория",
                               help_text="Родительская категория")

    icon = models.ImageField(blank=True,
                             null=True,
                             verbose_name="Иконка категории",
                             help_text="Иконка",
                             upload_to=category_icon_path,

                             validators=[
                                 FileExtensionValidator(
                                     allowed_extensions=['jpg', 'jpeg', 'png'],
                                     message="Разрешены только JPG, PNG"
                                 )],

                             error_messages={
                                 'invalid': 'Загрузите корректное изображение',
                                 'invalid_image': 'Файл поврежден или не является изображением',
                             })

    is_active = models.BooleanField(default=True, help_text="Категория активна", verbose_name="Активна")
    is_soft_deleted = models.BooleanField(default=False, help_text="Категория удалена", verbose_name="Удалена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self) -> str:
        """Читабельное представление модели в админ панели"""
        name = self.name
        return name

    def clean(self) -> None:
        """Дополнительная настройка и валидация"""
        super().clean()

        # Проверка вложенности (нельзя > 2)
        if self.parent and self.parent.parent:
            raise ValidationError("Нельзя создавать категорию глубже 2-ух уровней")

        # Проверка размера файла
        if self.icon and self.icon.size > 2 * 1024 * 1024:
            raise ValidationError({
                "icon": "Размер файла не должен превышать 2 МБ"
            })


class Product(models.Model):
    """Модель продуктов"""

    class Meta:
        """Настройка отображения в админке."""
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "-created_at", "updated_at"]

    name = models.CharField(max_length=255,
                            blank=False,
                            null=False,
                            db_index=True,
                            verbose_name="Продукт",
                            help_text="Название продукта",

                            error_messages={
                                "max_length": "Название не может быть больше 255 символов",
                                "blank": "Поле не может быть пустым",
                            })

    image = models.ImageField(blank=True,
                              null=True,
                              verbose_name="Изображение",
                              help_text="Изображение продукта",
                              upload_to=product_image_path,

                              validators=[
                                  FileExtensionValidator(
                                      allowed_extensions=['jpg', 'jpeg', 'png'],
                                      message="Разрешены только JPG, PNG"
                                  )],

                              error_messages={
                                  'invalid': 'Загрузите корректное изображение',
                                  'invalid_image': 'Файл поврежден или не является изображением',
                              })

    description = models.TextField(max_length=1500,
                                   blank=True,
                                   null=False,
                                   default="",
                                   verbose_name="Описание",
                                   help_text="Описание продукта",

                                   error_messages={
                                       "max_length": "Описание не может быть больше 1500 символов",
                                       "blank": "Поле не может быть пустым",
                                   })

    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                blank=False,
                                null=False,
                                verbose_name="Цена",
                                help_text="Цена продукта",

                                error_messages={
                                    "max_digits": "Цена не может быть больше 10 цифр",
                                    "blank": "Поле не может быть пустым",
                                })

    manufacturer = models.CharField(max_length=255,
                                   blank=False,
                                   null=False,
                                   verbose_name="Производитель",
                                   help_text="Имя производителя",

                                   error_messages={
                                       "max_length": "Название не может быть больше 255 символов",
                                       "blank": "Поле не может быть пустым",
                                   })
    sort_index = models.IntegerField(default=0,
                                     verbose_name="Индекс сортировки",
                                     blank=False,
                                     null=False,
                                     db_index=True,
                                     help_text="Чем меньше число, тем больше вероятность попасть на главную страницу",

                                     validators=[
                                         MinValueValidator(0, message="Индекс не может быть меньше 0"),
                                         MaxValueValidator(999, message="Индекс не может быть больше 999")
                                     ])
    is_limited_edition = models.BooleanField(default=False,
                                             db_index=True,
                                             verbose_name="Ограниченный тираж",
                                             help_text="Попадает в слайдер Limited edition на главной")

    is_soft_deleted = models.BooleanField(default=False, help_text="Продукт удален", verbose_name="Удален")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    category = models.ForeignKey(to=Category,
                                 on_delete=models.PROTECT,
                                 related_name="products",
                                 verbose_name="Категории",
                                 help_text="Категория товаров")

    def __str__(self):
        """Читабельное представление модели в админ панели"""
        return self.name

    @property
    def short_description(self) -> str:
        """Возвращает короткое описание продукта"""
        if self.description and len(self.description) > 100:
            return self.description[:100] + "..."
        return self.description

    def clean(self) -> None:
        """Дополнительная настройка и валидация"""
        super().clean()

        # Проверка размера файла
        if self.image and self.image.size > 2 * 1024 * 1024:
            raise ValidationError({
                "image": "Размер файла не должен превышать 2 МБ"
            })
