import redis
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from booking.models import Booking, BookingNotification
from booking.serializers import (
    BookingSerializer,
    ComplaintSerializer,
    NotificationSerializer,
    PaymentDetailsSerializer,
)

redis_instance = redis.StrictRedis(host="127.0.0.1", port=6379, db=1)


class BookAppointmentView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=["list bookings"],
        operation_description="Get the requested user bookings",
        responses={200: BookingSerializer, 400: "bad request", 500: "errors"},
    )
    def get(self, request):
        try:
            bookings = Booking.objects.filter(user=request.user).order_by("-booking_date")
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error":"No Booking is found"}, status=status.HTTP_404_NOT_FOUND)



    @swagger_auto_schema(
        tags=["Book professional"],
        operation_description="User book professional appointment",
        responses={200: BookingSerializer, 400: "bad request", 500: "errors"},
        request_body=BookingSerializer,
    )
    def post(self, request, professional_id):
        user = self.request.user
        # professional = get_object_or_404(User, pk=professional_id)
        professional = get_object_or_404(User, pk=professional_id)
        # request.data['user'] = user.id
        # request.data['professional'] = professional_id
        # serializer = BookingSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        booking_date = request.data.get("booking_date")
        address = request.data.get("address")
        job = request.data.get("job")
        price = request.data.get("price")
        try:
            booking = Booking.objects.create(
                user=user,
                professional=professional,
                booking_date=booking_date,
                address=address,
                job=job,
                price=price,
                is_paid=False,
                status=Booking.PENDING,
            )
            notification_message = (
                f"New booking from {user.username} for {job} on {booking_date}."
            )
            BookingNotification.objects.create(
                message=notification_message, user=professional
            )
            # channel_layer = get_channel_layer()
            # async_to_sync(channel_layer.group_send)(
            #     'notifications_group',
            #     {
            #         'type': 'send_notification',
            #         'message': 'New notification!',
            #     }
            # )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{professional.id}_notifications",
                {
                    "type": "send_notification",
                    "message": "New notification!",
                },
            )

            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfessionalBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["list bookings for professionals"],
        operation_description="Get the requested professional bookings",
        responses={200: BookingSerializer, 400: "bad request", 500: "errors"},
    )
    def get(self, request):
        try:
            professional_bookings = Booking.objects.filter(
                professional=request.user, status="pending"
            ).order_by("-booking_date")
            serializer = BookingSerializer(professional_bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error":"No Booking is found"}, status=status.HTTP_404_NOT_FOUND)


    @swagger_auto_schema(
        tags=["Professional booking confirmation "],
        operation_description="professional appointment confirmation",
        responses={200: BookingSerializer, 400: "bad request", 500: "errors"},
        request_body=BookingSerializer,
    )
    def post(self, request, booking_id, action):
        try:
            booking = Booking.objects.get(pk=booking_id, professional=request.user)

        except Booking.DoesNotExist:
            return Response(
                {"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if action == "confirm":
            booking.confirmed = True
            booking.status = Booking.CONFIRMED
            notification_message = f"Your booking is confirmed  {request.user.username} for {booking.job} on {booking.booking_date}."
            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                f"user_{booking.user.id}_notifications",
                {
                    "type": "send_notification",
                    "message": "New notification!",
                },
            )
        elif action == "cancel":
            notification_message = f"Your booking is cancelled  {request.user.username} for {booking.job} on {booking.booking_date}."
            BookingNotification.objects.create(
                message=notification_message, user=booking.user
            )
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{booking.user.id}_notifications",
                {
                    "type": "send_notification",
                    "message": "New notification!",
                },
            )

            booking.status = Booking.CANCELED
        else:
            return Response(
                {"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST
            )
        booking.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfessionalAcceptBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            professional_bookings = Booking.objects.filter(
                professional=request.user, status="confirmed", is_paid=False
            ).order_by("-booking_date")
            serializer = BookingSerializer(professional_bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error":"No Booking is found"}, status=status.HTTP_404_NOT_FOUND)



class CompleteWorkView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Professional complete booking"],
        operation_description="Professional complete appointment",
        responses={200: BookingSerializer, 400: "bad request", 500: "errors"},
        request_body=BookingSerializer,
    )
    def patch(self, request, booking_id):
        try:
            print(request.user, booking_id)
            booking = Booking.objects.get(pk=booking_id, professional=request.user)

        except Booking.DoesNotExist:
            return Response(
                {"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
            )

        payment_amount = request.data.get("payment_amount", None)

        if booking.status == Booking.CONFIRMED and payment_amount is not None:
            payment_serializer = PaymentDetailsSerializer(data=request.data)
            if payment_serializer.is_valid():
                booking.is_paid = True
                booking.price = payment_amount
                booking.save()
                notification_message = f"Your booking is completed {request.user.username} for {booking.job} on {booking.booking_date},Plz add confirmation."
                BookingNotification.objects.create(
                    message=notification_message, user=booking.user
                )
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"user_{booking.user.id}_notifications",
                    {
                        "type": "send_notification",
                        "message": "New notification!",
                    },
                )
                return Response(
                    {
                        "detail": "Confirmation details sent to the user",
                        # "booking_details": BookingSerializer(booking).data,
                        "payment_details": payment_serializer.validated_data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"detail": "Booking cannot be completed without a valid payment."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserAddConfirm(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["User confirmation"],
        operation_description="User Bookig complete confirmation",
        responses={200: BookingSerializer, 400: "bad request", 500: "errors"},
    )
    def get(self, request, booking_id):
        # print(booking_id)
        try:
            booking = Booking.objects.get(pk=booking_id, user=request.user)
            # print(booking,'lllll')
        except Booking.DoesNotExist:
            return Response(
                {"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if booking.status == Booking.CONFIRMED and booking.is_paid:
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Booking is not Completed please pay the price"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        tags=["User confirmation"],
        operation_description="User Bookig complete confirmation",
        responses={200: BookingSerializer, 400: "bad request", 500: "errors"},
        request_body=BookingSerializer,
    )
    # def put(self, request, booking_id, action):
    #     try:
    #         booking = Booking.objects.get(pk=booking_id, user=request.user)
    #     except Booking.DoesNotExist:
    #         return Response(
    #             {"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
    #         )

    #     if action == "confirm":
    #         booking.is_completed = True
    #         booking.status = Booking.COMPLETED

    #     elif action == "Incompleted":
    #         print(action)
    #         if booking.status == Booking.INCOMPLETED:
    #             booking.save()
    #             complaint_data = {
    #                 "user": request.user.id,
    #                 "booking": booking.id,
    #                 "description": request.data.get("description"),
    #             }
    #             complaint_serializer = ComplaintSerializer(data=complaint_data)

    #             if complaint_serializer.is_valid():
    #                 complaint_serializer.save()
    #                 return Response(
    #                     complaint_serializer.data, status=status.HTTP_201_CREATED
    #                 )
    #             else:
    #                 return Response(
    #                     complaint_serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #                 )
    #         else:
    #             return Response(
    #                 {"detail": "Invalid request for marking as incomplete"},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )

    #     else:
    #         return Response(
    #             {"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST
    #         )

    #     booking.save()
    #     serializer = BookingSerializer(booking)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, booking_id, action):
        try:
            booking = Booking.objects.get(pk=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response(
                {"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if action == "confirm":
            booking.is_completed = True
            booking.status = Booking.COMPLETED

        elif action == "Incompleted":
            booking.status = Booking.INCOMPLETED
            booking.save()
            complaint_data = {
                "user": request.user.id,
                "booking": booking.id,
                "description": request.data.get("description"),
            }
            complaint_serializer = ComplaintSerializer(data=complaint_data)

            if complaint_serializer.is_valid():
                complaint_serializer.save()
                return Response(
                    complaint_serializer.data, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    complaint_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST
            )

        booking.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Notification(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        notifications = BookingNotification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingData(APIView):
    def get(self, request):
        user_id = request.user.id
        cached_data = cache.get("user_bookings_{}".format(user_id))
        if cached_data is not None:
            return Response(cached_data, status=status.HTTP_200_OK)
        else:
            bookings = Booking.objects.filter(professional=request.user).order_by(
                "-booking_date"
            )
            serializer = BookingSerializer(bookings, many=True)
            cache.set("user_bookings_{}".format(user_id), serializer.data, timeout=3600)
            return Response(serializer.data, status=status.HTTP_200_OK)
