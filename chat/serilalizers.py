from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import User
from chat.models import Message





class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model =get_user_model()
        fields =['email','username','id']
        extra_kwargs ={'id':{'read_only':True}}

class MessageSerializer(serializers.ModelSerializer):
       class Meta:
           model = Message
           fields = ('id', 'username', 'message', 'timestamp','room','file')
           read_only_fields = ('id', 'timestamp')

# class MessageHistory(serializers.ModelSerializer):
#      class Meta:
#           model=Message
#           fields =['username','room']
 
