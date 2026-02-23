from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, UpdateAPIView, RetrieveAPIView, CreateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from lms.models import Course
from users.models import Payments, User, Subscription
from users.permissions import IsOwner
from users.serializers import PaymentsSerializer, UserSerializer, UserUpdateSerializer, UserForCreateSerializer, \
    SubscriptionSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


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


class PaymentsListAPIView(ListAPIView):
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
        stripe_product_id = create_stripe_product(payment)
        stripe_price_id = create_stripe_price(payment, stripe_product_id)
        payment.session_id, payment.link_pay = create_stripe_session(stripe_price_id)
        payment.save()


class SubscriptionCreateApiView(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'
        return Response({"message": message})