from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from .views import UserSignUpViewSet, EmailRegistrationView

router = SimpleRouter()
# router.register('auth/signup', UserSignUpViewSet, basename='auth-signup')
#

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('auth/signup/', EmailRegistrationView.as_view()),
]
