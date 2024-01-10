from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields=['username']


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model =get_user_model()
        fields =['email','username','id']
        extra_kwargs ={'id':{'read_only':True}}




from rest_framework import serializers
 
from chat.models import Message
 
 
class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()
 
    class Meta:
        model = Message
        fields = (
            "id",
            "conversation",
            "from_user",
            "to_user",
            "content",
            "timestamp",
            "read",
        )
 
    def get_conversation(self, obj):
        return str(obj.conversation.id)
 
    def get_from_user(self, obj):
        return UserSerializer(obj.from_user).data
 
    def get_to_user(self, obj):
        return UserSerializer(obj.to_user).data
