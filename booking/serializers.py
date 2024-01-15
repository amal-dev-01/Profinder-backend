from rest_framework import serializers

from booking.models import Booking, Complaint


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "user",
            "professional",
            "job",
            "address",
            "booking_date",
            "status",
            "price",
            "is_paid",
            "is_completed",
        ]


class PaymentDetailsSerializer(serializers.Serializer):
    payment_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ["user", "booking", "description", "status", "created_at"]
