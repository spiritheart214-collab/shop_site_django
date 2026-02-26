from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.db.models import Q

from .utils import avater_img_path


class User(AbstractUser):
    """Моделль пользователя"""

    name_validator = RegexValidator(
        regex=r'^[А-Яа-яA-Za-z-]+$',
        message="Только буквы"
    )

    first_name = models.CharField(max_length=150,
                                  blank=True,
                                  null=True,
                                  db_index=True,
                                  verbose_name="Имя",
                                  help_text="Введите имя",

                                  validators=[name_validator],

                                  error_messages={
                                      "max_length": "Имя не может быть больше 150 символов",
                                  })

    last_name = models.CharField(max_length=150,
                                 blank=True,
                                 null=True,
                                 verbose_name="Фамилия",
                                 help_text="Введите фамилию",

                                 validators=[name_validator],

                                 error_messages={
                                     "max_length": "Фамилия не может быть больше 150 символов",
                                 })

    patronymic = models.CharField(max_length=150,
                                  blank=True,
                                  verbose_name="Отчество",
                                  help_text="Введите отчество",

                                  validators=[name_validator],

                                  error_messages={
                                      "max_length": "Отчество не может быть больше 150 символов",
                                  })

    email = models.EmailField(max_length=254,
                              blank=True,
                              null=True,
                              unique=False,
                              help_text="Введите Email",
                              verbose_name="Email",

                              error_messages={
                                  "max_length": "Email не может быть больше 254 символов",
                                  "invalid": "Введите корректны Email (name@domain.com)",
                                  "blank": "Поле не может быть пустым"
                              })

    telephone = models.CharField(max_length=20,
                                 blank=True,
                                 null=True,
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
                                     "blank": "Поле не может быть пустым"
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
    REQUIRED_FIELDS = ['email', 'telephone']

    def __str__(self) -> str:
        """Отображение в админке"""
        if self.full_name:
            return self.full_name
        if self.email:
            return self.email
        return f"Пользователь {self.pk}"

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
        """
        Настройка отображения в админке.
        Настройка уникальности для телефона, email.
        Поля должны быть уникальными если их заполняют. Иначе поля будут пусты для каждого пользователя
        """
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]

# Todo сделать возможной регистрацию бех указании номера телфона и почты
