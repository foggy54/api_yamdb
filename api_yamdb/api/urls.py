from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import EmailRegistrationView, RetrieveAccessToken, UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet, basename='auth-users')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', EmailRegistrationView.as_view()),
    path(
        'auth/token/', RetrieveAccessToken.as_view(), name='token_obtain_pair'
    ),
]
