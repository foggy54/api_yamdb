import random
import string

from django import views
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EmailRegistration, UserSerializer

TOKEN_LEN = 8
User = get_user_model()


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

        access_code = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits
            )
            for _ in range(TOKEN_LEN)
        )

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            user, created = User.objects.get_or_create(
                email=email, username=username
            )
            user.access_code = access_code
            user.save()
            if created:
                title_email = 'YAMDB access code.'
            else:
                title_email = 'YAMDB access code has been renewed.'
            from_email = 'admin@yamdb.com'
            text = (
                f'Hello, please use your username: {username} and access code: {access_code} to \n'
                f'get the access to the site via the link /api/v1/auth/token/'
            )
            send_mail(
                title_email,
                text,
                from_email,
                [
                    email,
                ],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
