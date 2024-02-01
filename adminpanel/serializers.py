from rest_framework import serializers

from adminpanel.models import Payment


class PaymentSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

