from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models

from .utils import avater_img_path


class User(AbstractUser):
    """Моделль пользователя"""

    first_name = models.CharField(max_length=150,
                                  blank=False,
                                  null=False,
                                  db_index=True,
                                  verbose_name="Имя",
                                  help_text="Введите имя",

                                  error_messages={
                                      "max_length": "Имя не может быть больше 150 символов",
                                      "blank": "Имя обязателено для заполнения",
                                  })

    last_name = models.CharField(max_length=150,
                                 blank=False,
                                 null=False,
                                 verbose_name="Фамилия",
                                 help_text="Введите фамилию",

                                 error_messages={
                                     "max_length": "Фамилия не может быть больше 150 символов",
                                     "blank": "Фамилия обязателена для заполнения",
                                 })

    patronymic = models.CharField(max_length=150,
                                  blank=True,
                                  verbose_name="Отчество",
                                  help_text="Введите отчество",

                                  error_messages={
                                      "max_length": "Отчество не может быть больше 150 символов",
                                  })

    email = models.EmailField(max_length=254,
                              blank=False,
                              null=False,
                              unique=True,
                              help_text="Введите Email",
                              verbose_name="Email",

                              error_messages={
                                  "max_length": "Email не может быть больше 254 символов",
                                  "blank": "Email обязателен для заполнения",
                                  "unique": "Пользователь с таким email уже зарегестрирован",
                                  "invalid": "Введите корректны Email (name@domain.com)"
                              })

    telephone = models.CharField(max_length=20,
                                 blank=False,
                                 null=False,
                                 unique=True,
                                 verbose_name="Телефон",
                                 help_text="Введите номер телефон",

                                 validators=[
                                     RegexValidator(
                                         regex=r'^\+?7?\d{10,15}$',
                                         message="Введите номер в формате: +79991234567 или 89991234567"
                                     )],

                                 error_messages={
                                     "max_length": "Слишком много символов",
                                     "blank": "Телефон обязателен для заполнения",
                                     "unique": "Пользователь с таким телефоном уже зарегистрирован",
                                 })

    avatar = models.ImageField(blank=True,
                               null=True,
                               verbose_name="Аватар",
                               help_text="Загрузите фото профиля",
                               upload_to=avater_img_path,

                               validators=[
                                   FileExtensionValidator(
                                       allowed_extensions=['jpg', 'jpeg', 'png'],
                                       message="Разрешены только JPG, PNG"
                                   )],

                               error_messages={
                                   'invalid': 'Загрузите корректное изображение',
                                   'invalid_image': 'Файл поврежден или не является изображением',
                               })

    # Настройки входа (создания суперпользователя)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telephone', "email"]

    def __str__(self) -> str:
        """Отображение в админке"""
        user = f"{self.last_name} {self.first_name}"
        return user

    @property
    def full_name(self) -> str:
        """
        Возвращает полное имя пользователя
        """
        parts = [self.last_name, self.first_name, self.patronymic]
        filtered_full_name = " ".join(filter(None, parts))
        return filtered_full_name

    def clean(self) -> None:
        """Дополнительная настройка и валидация"""
        super().clean()

        if self.email:
            self.email = self.email.lower()

            # Проверка размера файла
        if self.avatar and self.avatar.size > 2 * 1024 * 1024:
            raise ValidationError({
                "avatar": "Размер файла не должен превышать 2 МБ"
            })

    class Meta:
        """Настройка отображения в админке"""
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]
