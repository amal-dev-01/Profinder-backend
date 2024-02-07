from django.contrib.auth import get_user_model
from rest_framework import serializers

from chat.models import Message, Room


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "username", "id"]
        extra_kwargs = {"id": {"read_only": True}}


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "username", "message", "timestamp", "room", "file")
        read_only_fields = ("id", "timestamp")


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
