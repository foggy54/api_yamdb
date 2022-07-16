import secrets
import string

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Review, Title

from .permissions import IsAdmin, IsAuthorModeratorAdminOrReadOnly, IsSelf
from .serializers import (
    CommentsSerializer,
    EmailRegistration,
    LoginUserSerializer,
    ReviewSerializer,
    UserSelfSerializer,
    UserSerializer,
)
from .utilities import send_token_email
from .validators import NotFoundValidationError

CODE_LEN = 20
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=['patch', 'get'],
        permission_classes=[IsSelf],
    )
    def me(self, request, pk=None):
        if request.method == 'GET':
            instance = self.request.user
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        if request.method == 'PATCH':
            partial = True
            instance = self.request.user
            serializer = UserSelfSerializer(
                instance, data=request.data, partial=partial
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class EmailRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = EmailRegistration(data=request.data)

        access_code = ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(CODE_LEN)
        )

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            user, created = User.objects.get_or_create(
                email=email, username=username
            )
            user.access_code = make_password(
                access_code, salt=None, hasher='default'
            )
            user.save()
            send_token_email(username, access_code, email, created)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveAccessToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
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

            refresh = RefreshToken.for_user(user)
            return Response(
                {'access': str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorModeratorAdminOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (
        IsAuthorModeratorAdminOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, review=review)
