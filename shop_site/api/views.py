from django_filters.rest_framework import  DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter

from users.models import User
from .serializers import UsersSerializer


class UsersViewSet(ModelViewSet):
    """Набор представлений для дейтсвий над пользовтаелями"""

    queryset = User.objects.only("id", 'first_name', "last_name", "patronymic", "email", "telephone").all()
    serializer_class = UsersSerializer

    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ["first_name",  "last_name", "email", "telephone"]
    search_fields = ["first_name", "last_name", "email", "telephone"]
    filterset_fields = ["first_name",  "last_name", "email", "telephone"]
