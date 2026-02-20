from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View


class HelloWorldView(View):
    """Временная страница. Для ридиректов и тестов"""

    def get(self, requests: HttpRequest) -> HttpResponse:
        """Вывод Hello world!"""
        return HttpResponse("Hello world!")
