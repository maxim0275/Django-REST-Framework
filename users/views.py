from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView)

from users.models import Payments
from users.serializers import PaymentsSerializer


class PaymentListView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['course_paid', 'lesson_paid', 'payment_method']
    search_fields = ['course_paid', 'lesson_paid', 'payment_method']
    ordering_fields = ['date']
