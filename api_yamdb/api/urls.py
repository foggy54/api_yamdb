from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (EmailRegistrationView, RetrieveAccessToken, ReviewViewSet,
                    UserViewSet)

v1_router = SimpleRouter()
v1_router.register('users', UserViewSet, basename='auth-users')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)


urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup/', EmailRegistrationView.as_view()),
    path(
        'vauth/token/', RetrieveAccessToken.as_view(), name='token_obtain_pair'
    ),
]
