from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from .views import UserSignUpViewSet, EmailRegistrationView, ReviewViewSet

router = SimpleRouter()
# router.register('auth/signup', UserSignUpViewSet, basename='auth-signup')
v1_router = SimpleRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(v1_router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/auth/signup/', EmailRegistrationView.as_view()),
]
