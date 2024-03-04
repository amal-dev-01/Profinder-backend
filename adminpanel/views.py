import logging
from datetime import datetime

import stripe
from django.db.models import Q
# from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from account.serializers import UserSerializer
from adminpanel.models import Payment
from adminpanel.serializers import PaymentSerilaizer
from booking.models import Booking
from booking.serializers import BookingSerializer
from profinder.settings import FRONT_END_URL, STRIPE_SECRET

# Create your views here.

logger = logging.getLogger("django")


class UserList(generics.ListAPIView):
    queryset = User.objects.filter(is_user=True)
    serializer_class = UserSerializer


class ProfessionlList(generics.ListAPIView):
    queryset = User.objects.filter(is_professional=True)
    serializer_class = UserSerializer


class UsersDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingFilterView(APIView):
    @swagger_auto_schema(
        tags=["Booking search"],
        operation_description="Booking details",
        responses={200: BookingSerializer, 400: "bad request", 500: "errors"},
    )
    def get(self, request, action):
        bookings = Booking.objects.filter(status=action)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingDetails(APIView):
    @swagger_auto_schema(
        tags=["Booking details"],
        operation_description="Booking details",
        responses={200: BookingSerializer, 400: "bad request", 500: "errors"},
    )
    def get(self, request, pk):
        try:
            booking = Booking.objects.filter(id=pk).first()
        except Booking.DoesNotExist:
            return Response(
                {"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)


stripe.api_key = STRIPE_SECRET


class AdminPayment(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Payment price"],
        operation_description="Get the payment",
        responses={200: PaymentSerilaizer, 400: "bad request", 500: "errors"},
    )
    def get(self, request):
        try:
            payment = Payment.objects.get(
                Q(professional=request.user),
                Q(month=datetime.now().month, year=datetime.now().year),
            )

        except Payment.DoesNotExist:
            return Response(
                {"detail": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = PaymentSerilaizer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Professional payment"],
        operation_description="professional payment to admin",
        responses={200: PaymentSerilaizer, 400: "bad request", 500: "errors"},
        request_body=PaymentSerilaizer,
    )
    def post(self, request):
        # serializer = PaymentSerilaizer()
        try:
            payment = Payment.objects.get(
                Q(professional=request.user),
                Q(month=datetime.now().month, year=datetime.now().year),
            )
            print(payment)

        except Payment.DoesNotExist:
            return Response(
                {"detail": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        product = stripe.Product.create(name="Subscription", type="service")

        price = stripe.Price.create(
            unit_amount=int(payment.total_amount * 100),
            product=product.id,
            currency="usd",
        )

        customer = stripe.Customer.create(
            email=request.user.email, name=request.user.username
        )

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price.id,
                        "quantity": 1,
                    },
                ],
                mode="payment",
                customer=customer.id,
                success_url=f"{FRONT_END_URL}success/?success=true&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=FRONT_END_URL + "?canceled=true",
            )
            payment.stripe_id = checkout_session.id
            payment.save()
            return Response({"url": checkout_session.url}, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentSuccessView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Professional payment"],
        operation_description="professional payment to admin success",
        responses={200: PaymentSerilaizer, 400: "bad request", 500: "errors"},
        request_body=PaymentSerilaizer,
    )
    def post(self, request):
        session_id = request.data.get("session_id")
        payment = Payment.objects.get(stripe_id=session_id)
        payment.status = "completed"
        payment.save()
        user = payment.professional
        user.is_blocked = False
        user.save()

        return Response({"msg": "Completed Successfully"}, status=status.HTTP_200_OK)


class ProfessionalPayment(APIView):
    def get(self, request):
        try:
            payment = Payment.objects.all()
            serializer = PaymentSerilaizer(payment, many=True)
            return Response(serializer.data)
        except Payment.DoesNotExist:
            return Response({"error":"Not payment is found"},status=status.HTTP_404_NOT_FOUND)












# from django.db.models import Sum
# from django.db.models.functions import TruncMonth
# from rest_framework.views import APIView
# from booking.models import Booking


# class Total(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             result = (
#                 Booking.objects.filter(status=Booking.COMPLETED, is_paid=True)
#                 .annotate(month=TruncMonth("booking_date"))
#                 .values("professional", "month")
#                 .annotate(total_amount=Sum("price"))
#                 .order_by("professional", "month")
#             )
#             logger.info(level=logging.INFO, msg="Successfully retrieved total data")
#             logger.debug("This is a debug message")
#             logger.info("This is an informational message")
#             logger.warning("This is a warning message")
#             logger.critical("This is a critical message")

#             return Response({"result": result}, status=status.HTTP_200_OK)
#         except Exception as e:
#             logger.error("An error occurred while retrieving total data: %s", str(e))
#             return Response(
#                 {"error": "An error occurred"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

