from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from chat.serilalizers import MessageSerializer, UserGetSerializer,RoomSerializer

from .models import Message,Room

# Create your views here.


class ListUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_obj = User.objects.exclude(id=request.user.id)
            serializer = UserGetSerializer(user_obj, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            print("error", str(e))
            return Response({"error": "Error in getting user list"}, status=400)


class MessageList(APIView):
    def get(self, request, format=None):
        messages = Message.objects.all().order_by("-timestamp")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, message_id, format=None):
        try:
            message = Message.objects.get(pk=message_id)
        except Message.DoesNotExist:
            return Response(
                {"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND
            )

        message.delete()
        return Response(
            {"message": "Message deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ChatHistoryView(APIView):
    def get(self, request, room_name):
        try:
            chat_history = Message.objects.filter(room__name=room_name).order_by(
                "timestamp"
            )
            serializer = MessageSerializer(chat_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteMessageView(APIView):
    def delete(self, request, message_id):
        try:
            message = Message.objects.get(pk=message_id)
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response(
                {"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChatNotification(APIView):
    def get(self, request):
        rooms = Room.objects.filter(name__contains=request.user.username)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class Notification(APIView):
#     def get(request):
#     return Response(request, 'index.html')
