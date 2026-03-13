def category_icon_path(instance: "Category", filename: str) -> str:
    """
    Генерация пути, где будет сохранена иконка категории

    :param instanse: Обьект Category
    :param filename: Имя файла
    :return: путь в виде текста (str)
    """

    url = f"products/categories/icons/{filename}"
    return url


def product_image_path(instance: "Product", filename: str) -> str:
    """
    Генерация пути, где будет сохранено изображение продукта

    :param instanse: Обьект Product
    :param filename: Имя файла
    :return: путь в виде текста (str)
    """

    url = f"products/products/image/{filename}"
    return url
