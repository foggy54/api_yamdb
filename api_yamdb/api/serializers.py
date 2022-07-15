from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import MAX_LENGTH_LONG, MAX_LENGTH_MED, Review, Comment

from .validators import username_restriction, role_restriction

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_MED,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            username_restriction,
        ],
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_LONG,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'bio',
        )
        model = User


class UserSelfSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_MED,
        validators=[
            UniqueValidator(
                queryset=User.objects.filter(access_code__isnull=False)
            ),
            username_restriction,
        ],
        required=False,
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_LONG,
        validators=[
            UniqueValidator(
                queryset=User.objects.filter(access_code__isnull=False)
            )
        ],
        required=False,
    )
    role = serializers.CharField(
        max_length=MAX_LENGTH_MED,
        read_only=True,
    )

    class Meta:
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role',
        )
        model = User


class EmailRegistration(serializers.Serializer):
    email = serializers.EmailField(
        max_length=MAX_LENGTH_LONG,
    )
    username = serializers.CharField(
        max_length=MAX_LENGTH_MED,
        validators=[
            username_restriction,
        ],
    )


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(write_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        user = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise serializers.ValidationError(
                'Отзыв создан. Можно создавать только один отзыв.'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'pub_date', 'author')
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
