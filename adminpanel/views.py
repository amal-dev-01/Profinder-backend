from rest_framework import generics, status
from rest_framework.response import Response

from account.models import User
from account.serializers import UserSerializer

# Create your views here.


class UserList(generics.ListAPIView):
    queryset = User.objects.filter(is_user=True)
    serializer_class = UserSerializer


class ProfessionlList(generics.ListAPIView):
    queryset = User.objects.filter(is_professional=True)
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)




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



from adminpanel.tasks import send_mail_func
from django.shortcuts import HttpResponse

def send_mail_to_users(request):
    send_mail_func.delay()
    return HttpResponse('sent')




