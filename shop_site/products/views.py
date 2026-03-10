from django.http import HttpResponse, HttpRequest
from django.views import View


class HelloWorldView(View):
    """Обработка стартовой страницы"""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Получть страницу"""
        return HttpResponse("Hello product world!")
