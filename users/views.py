from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, UpdateAPIView, RetrieveAPIView, CreateAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import Payments, User
from users.permissions import IsOwner
from users.serializers import PaymentsSerializer, UserSerializer, UserUpdateSerializer, UserForCreateSerializer


class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserForCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class UserRetrieveApiView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        instance = self.get_object()
        if instance.id == self.request.user.id:
            serializer = super().get_serializer_class()
        else:
            serializer = UserUpdateSerializer
        return serializer


class PaymentListView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['course_paid', 'lesson_paid', 'payment_method']
    search_fields = ['course_paid', 'lesson_paid', 'payment_method']
    ordering_fields = ['date']


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user_payer=self.request.user)
        payment.save()
