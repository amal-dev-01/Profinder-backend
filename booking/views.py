from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from booking.serializers import BookingSerializer,PaymentDetailsSerializer
from booking.models import Booking
from account.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django.core.mail import send_mail



class BookAppointmentView(APIView):
    permission_classes=(IsAuthenticated,)
    
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, professional_id):
        user = self.request.user
        professional = get_object_or_404(User, pk=professional_id)
        booking_date = request.data.get('booking_date')
        address = request.data.get('address')
        job = request.data.get('job')
        price = request.data.get('price')
        try:
            booking = Booking.objects.create(
                user=user,
                professional=professional,
                booking_date=booking_date,
                address=address,
                job=job,
                price=price,
                is_paid=False,
                status=Booking.PENDING
            )
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class ProfessionalBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request): 
        professional_bookings = Booking.objects.filter(professional=request.user)
        serializer = BookingSerializer(professional_bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request, booking_id, action):
        try:
            booking = Booking.objects.get(pk=booking_id,professional = request.user)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        if action == 'confirm':
            booking.confirmed = True
            booking.status = Booking.CONFIRMED
        elif action == 'cancel':
            booking.status = Booking.CANCELED
        else:
            return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        booking.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompleteWorkView(APIView):
    def patch(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, professional=request.user)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        payment_amount = request.data.get('payment_amount', None)

        if booking.status == Booking.CONFIRMED and payment_amount is not None:
            payment_serializer = PaymentDetailsSerializer(data=request.data)
            if payment_serializer.is_valid():
                # send_confirmation_details_to_user(booking, payment_serializer.validated_data)                
                return Response({
                    "detail": "Confirmation details sent to the user",
                    # "booking_details": BookingSerializer(booking).data,
                    # "payment_details": payment_serializer.validated_data
                }, status=status.HTTP_200_OK)
            else:
                return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Booking cannot be completed without a valid payment."}, status=status.HTTP_400_BAD_REQUEST)



 



class UserAddConfirm(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if booking.status == Booking.CONFIRMED and booking.is_paid:
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Booking is not Completed please pay the price"}, status=status.HTTP_400_BAD_REQUEST)

            








    




    