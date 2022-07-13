from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from .views import (
    UserViewSet,
    EmailRegistrationView,
    RetrieveAccessToken,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = SimpleRouter()  # не знаю, нужно ли это тут, но пока добавил
router.register('users', UserViewSet, basename='auth-users')
#

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', EmailRegistrationView.as_view()),
    path(
        'auth/token/', RetrieveAccessToken.as_view(), name='token_obtain_pair'
    ),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
