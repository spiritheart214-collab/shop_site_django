from django_filters.rest_framework import  DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter

from users.models import User
from .serializers import UsersSerializer


@extend_schema_view(
    list=extend_schema(tags=["API Users"]),
    retrieve=extend_schema(tags=["API Users"]),
    create=extend_schema(tags=["API Users"]),
    update=extend_schema(tags=["API Users"]),
    partial_update=extend_schema(tags=["API Users"]),
    destroy=extend_schema(tags=["API Users"]),
)
class UsersViewSet(ModelViewSet):
    """Набор представлений для дейтсвий над пользовтаелями"""

    queryset = User.objects.only("id", 'first_name', "last_name", "patronymic", "email", "telephone").all()
    serializer_class = UsersSerializer

    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ["first_name",  "last_name", "email", "telephone"]
    search_fields = ["first_name", "last_name", "email", "telephone"]
    filterset_fields = ["first_name",  "last_name", "email", "telephone"]

