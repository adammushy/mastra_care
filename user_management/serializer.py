from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.forms import PasswordChangeForm


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =[
            'id',
            'username',
            'name',
            'email',
            'phone',
            'blood_group',
            'dob',
            'height',
            'gender',
            'profile',
            'profile_binary',
            'password',
            
        ]
        extra_kwargs={"password":{"write_only":True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
