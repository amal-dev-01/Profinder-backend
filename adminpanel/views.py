from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from account.models import User
from account.serializers import UserSerializer
from booking.models import Booking
from booking.serializers import BookingSerializer
from adminpanel.models import Payment
from datetime import datetime,date,time
from django.db.models import Q
from adminpanel.serializers import PaymentSerilaizer
from rest_framework.permissions import IsAuthenticated
import stripe
from django.shortcuts import get_object_or_404
from profinder.settings import STRIPE_SECRET
from profinder.settings import FRONT_END_URL

# Create your views here.


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
    serializer_class =BookingSerializer


class BookingFilterView(APIView):
    def get(self,request,action):
        bookings = Booking.objects.filter(status=action)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class BookingDetails(APIView):
    def get(self,request,pk):
        try:
            booking = Booking.objects.filter(id=pk).first()
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)



stripe.api_key = STRIPE_SECRET

class AdminPayment(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        try:
            payment = Payment.objects.get(
                Q(professional=request.user),
                Q(month=datetime.now().month, year=datetime.now().year)
            )

        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer =PaymentSerilaizer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self,request):
        serializer= PaymentSerilaizer()
        try:
            payment = Payment.objects.get(
                Q(professional=request.user),
                Q(month=datetime.now().month, year=datetime.now().year)
            )
            print(payment)

        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        product = stripe.Product.create(
            name='Subscription',
            type='service'
        )

        price = stripe.Price.create(
            unit_amount=int(payment.total_amount * 100),
            product=product.id,
            currency='usd',
        )

        customer = stripe.Customer.create(
            email=request.user.email,
            name=request.user.username  
        )

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                customer=customer.id,
                success_url = f"{FRONT_END_URL}success/?success=true&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=FRONT_END_URL + '?canceled=true',

                )
            payment.stripe_id = checkout_session.id
            payment.save()
            return Response({'url': checkout_session.url}, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentSuccessView(APIView):
    permission_classes =[IsAuthenticated]
    def post(self, request):
        session_id = request.data.get('session_id')
        payment = get_object_or_404(Payment, stripe_id=session_id)
        payment.status ='completed'
        payment.save()        
        user = payment.professional
        user.is_blocked = False
        user.save()


        return Response({"msg": "Completed Success fully"}, status=status.HTTP_200_OK)



from django.db.models import Sum
from django.db.models.functions import TruncMonth
from booking.models import Booking
from rest_framework.views import APIView

class Total(APIView):

    def get(self,request, *args, **kwargs):
        result = (
            Booking.objects.filter(status=Booking.COMPLETED, is_paid=True)
            .annotate(month=TruncMonth('booking_date'))
            .values('professional', 'month')  
            .annotate(total_amount=Sum('price'))
            .order_by('professional', 'month')  
        )



# from adminpanel.tasks import send_mail_func
# from django.shortcuts import HttpResponse

# def send_mail_to_users(request):
#     send_mail_func.delay()
#     return HttpResponse('sent')


# class BlockOverdueProfessionalsAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         overdue_professionals = User.objects.filter(
#             is_professional =True,
#             payment__status=Payment.PENDING,
#             payment__month__lt=(date.today().month - 1),
#             payment__year=date.today().year
#         ).distinct()

#         for professional in User.objects.filter(is_professional =True):
#             if professional in overdue_professionals:
#                 professional.is_blocked = True
#             else:
#                 professional.is_blocked = False

#             professional.save()
#         return Response({"message": "Professionals blocked or unblocked based on payment status."}, status=status.HTTP_200_OK)
