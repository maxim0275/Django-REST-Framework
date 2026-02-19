from rest_framework.serializers import ModelSerializer

from users.models import Payments, User, Subscription


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(ModelSerializer):
    history_payments = PaymentsSerializer(
        source="payments",
        many=True,
    )

    class Meta:
        model = User
        fields = "__all__"


class UserForCreateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserUpdateSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ("password", "last_name")

class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
