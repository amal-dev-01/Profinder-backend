from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import User
from chat.serilalizers import UserGetSerializer,MessageSerializer
from .models import Message


# Create your views here.

class ListUser(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            user_obj= User.objects.exclude(id=request.user.id)
            serializer = UserGetSerializer(user_obj,many = True)
            return Response(serializer.data,status=200)
        except Exception as e:
            print('error',str(e))
            return Response({'error':"Error in getting user list"},status=400)
        

# from rest_framework import generics
# # from .models import Message
 

# class MessageList(generics.ListCreateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     ordering = ('-timestamp',)
        
from rest_framework import generics
from .models import Message

class MessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
