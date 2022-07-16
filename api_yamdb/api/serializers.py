from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import MAX_LENGTH_LONG, MAX_LENGTH_MED, Comment, Review

from .validators import NotFoundValidationError, username_restriction

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
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_LONG,
        validators=[
            UniqueValidator(
                queryset=User.objects.filter(access_code__isnull=False)
            )
        ],
        required=True,
    )
    role = serializers.CharField(max_length=MAX_LENGTH_MED, read_only=True)

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

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        duplicate_email = (
            User.objects.filter(Q(email=email))
            .filter(~Q(username=username))
            .exists()
        )
        duplicate_username = (
            User.objects.filter(Q(username=username))
            .filter(~Q(email=email))
            .exists()
        )
        if duplicate_email:
            raise serializers.ValidationError(
                {'detail': 'Email is already taken.'}
            )
        if duplicate_username:
            raise serializers.ValidationError(
                {'detail': 'Username is already taken.'}
            )
        return data


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(username=data['username']).first()
        if user == None:
            raise NotFoundValidationError({'detail': 'User not found'})
        check_access_code = check_password(
            data['confirmation_code'], user.access_code
        )
        if not check_access_code:
            raise serializers.ValidationError(
                {'detail': 'Incorrect username or access_code'}
            )
        return data


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
                'It is not allowed to create multiple reviews for same user'
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
