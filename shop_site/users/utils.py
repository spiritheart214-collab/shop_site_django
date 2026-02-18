from typing import Optional


def avater_img_path(instance: Optional['User'], filename: str) -> str:
    """
    Генерация пути, где будет сохранен аватар пользователя

    :param instanse: Обьект User
    :param filename: Имя файла
    :return: путь в виде текста (str)
    """
    email = instance.email.replace("@", "_at_")
    url = f"users/user_{email}/avatar/{filename}"
    return url
