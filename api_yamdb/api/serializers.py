from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .validators import username_restriction

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'password')
        model = User


class EmailRegistration(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        max_length=50,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            username_restriction,
        ],
    )


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(write_only=True)
