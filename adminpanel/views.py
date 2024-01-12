from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from account.serializers import UserSerializer
from rest_framework import generics



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

    




