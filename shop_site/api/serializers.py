from rest_framework import serializers
from users.models import User


class UsersSerializer(serializers.ModelSerializer):
    """Единый сериализатор с разными полями для чтения/записи"""

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "patronymic",

            "full_name",
            "email",
            "telephone",
            "date_joined",
        )
        extra_kwargs = {
            'password': {'write_only': True},  # скрываем при GET
            'username': {'write_only': True},  # скрываем при GET
            'first_name': {'write_only': True},  # скрываем при GET
            'last_name': {'write_only': True},  # скрываем при GET
            'patronymic': {'write_only': True},  # скрываем при GET
        }

    def to_representation(self, instance):
        """Переопределяем, что показывать при GET"""
        data = super().to_representation(instance)

        data_get = {
            'full_name': data['full_name'],
            'email': data['email'],
            'telephone': data['telephone'],
            "date_joined": data["date_joined"]
        }

        return data_get

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
