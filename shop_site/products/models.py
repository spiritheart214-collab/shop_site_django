from django.core.validators import FileExtensionValidator
from django.db import models
from django.core.exceptions import ValidationError

from .utils import category_icon_path


class Category(models.Model):
    """Модель категорий товаров"""

    class Meta:
        """Настройка отображения в админке."""
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    name = models.CharField(max_length=255,
                            blank=False,
                            null=False,
                            db_index=True,
                            verbose_name="Категория",
                            help_text="Название категории",

                            error_messages={
                                "max_length": "Название не может быть больше 255 символов",
                                "blank": "Поле не может быть пустым",
                                "unique": "Такая  категория уже существует",
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

    def __str__(self) -> str:
        """Читабельное представление модели в админ панели"""
        name = self.name
        return name

    def clean(self) -> None:
        """Дополнительная настройка и валидация"""
        super().clean()

        if self.parent and self.parent.parent:
            raise ValidationError("Нельзя создавать категорию глубже 2-ух уровней")
