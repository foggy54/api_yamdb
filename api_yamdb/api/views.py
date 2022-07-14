import random
import string

from django import views
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail

from .models import User, Title
from .permissions import IsAuthorModeratorAdminOrReadOnly
from .serializers import EmailRegistration, UserSerializer, ReviewSerializer

TOKEN_LEN = 8


class UserSignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        username = self.kwargs.get('username')
        password = self.kwargs.get('password')
        serializer.save(username=username, password=password)


class EmailRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = EmailRegistration(data=request.data)

        token = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits
            )
            for _ in range(TOKEN_LEN)
        )

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            text = (
                f'Hello, please send your username: {username} and token {token} to \n'
                f'/api/v1/auth/token/ in order to complete the registration process.'
            )
            send_mail(
                'Registration attempt.',
                text,
                'from@example.com',  # Это поле "От кого"
                [
                    email,
                ],  # Это поле "Кому" (можно указать список адресов)
                fail_silently=False,  # Сообщать об ошибках («молчать ли об ошибках?»)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (
    #     IsAuthorModeratorAdminOrReadOnly,
    #     permissions.IsAuthenticatedOrReadOnly,
    # )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
