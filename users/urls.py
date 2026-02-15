from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserCreateApiView, UserUpdateApiView, UserRetrieveApiView, PaymentCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', UserCreateApiView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),

    path("<int:pk>/update/", UserUpdateApiView.as_view(), name="users-update"),
    path("<int:pk>/", UserRetrieveApiView.as_view(), name="users-retrieve"),

    # payments
    path("payment/", PaymentCreateAPIView.as_view(), name="payment"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments-list"),
]