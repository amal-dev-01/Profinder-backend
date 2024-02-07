from rest_framework import serializers

from booking.models import Booking, BookingNotification, Complaint


class BookingSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source="user.username")
    professional_name = serializers.ReadOnlyField(source="professional.username")

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "professional",
            "job",
            "address",
            "booking_date",
            "status",
            "price",
            "is_paid",
            "is_completed",
            "user_name",
            "professional_name",
        ]

    # def create(self, validated_data):
    #     booking = Booking.objects.create(**validated_data)
    #     return booking


class PaymentDetailsSerializer(serializers.Serializer):
    payment_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ["user", "booking", "description", "status", "created_at"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingNotification
        fields = "__all__"
