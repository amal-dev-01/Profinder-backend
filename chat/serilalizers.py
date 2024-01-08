from rest_framework import serializers
from django.contrib.auth import get_user_model



class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model =get_user_model()
        fields =['email','username','id']
        extra_kwargs ={'id':{'read_only':True}}
