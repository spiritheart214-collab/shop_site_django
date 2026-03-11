"""Модуль с реализующий парсинг импортируемого файла и создание категорий на его основе"""
from csv import DictReader
from io import TextIOWrapper
from typing import Dict, List, Union

from django.core.files.uploadedfile import UploadedFile
from django.db import IntegrityError

from ..models import Category


def parse_csv(uploaded_file: UploadedFile) -> List[Dict[str, str]]:
    """Читает CSV файл и превращает в список словарей"""
    csv_file = TextIOWrapper(uploaded_file, encoding="utf-8-sig")
    csv_reader: List[Dict[str, str]] = list(DictReader(csv_file))
    return csv_reader


def create_categories(сategories_list: List[Dict[str, str]]) -> Dict[str, Union[int, List[str]]]:
    """
    Создаёт категории из списка данных.

    Возвращает:
        tuple:
            - количество успешно созданных категорий
            - список ошибок
    """
    print(сategories_list)
    success_count: int = int()
    errors: List[str] = list()

    for index, category in enumerate(сategories_list, start=1):
        print(index)
        print(category)

        try:

            parent_name = category.get("parent")
            parent_obj = None

            if parent_name:
                parent_obj = Category.objects.filter(name=parent_name).first()

            Category.objects.create(
                name=category.get("name"),
                parent=parent_obj,
                is_active=str_to_bool(category.get("is_active")),
                is_soft_deleted=str_to_bool(category.get("is_soft_deleted"))
            )
            success_count += 1
        except IntegrityError as error:
            errors.append(f"Строка: {index}\n"
                          f"Ошибка: {str(error)}")
        except Exception as error:
            errors.append(f"Строка {index}: {str(error)}")

    category_data = {
        "success": success_count,
        "errors": errors
    }

    return category_data


def str_to_bool(value: str) -> bool:
    """Конвертирует строку CSV в bool"""
    if value is None or value == '':
        return False
    return str(value).lower() in ("true", "1", "yes", "да")

    # Todo добавить сервис перевода для ошибок ?!
