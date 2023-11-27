from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import AuthUser

class AuthUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = AuthUser
        fields = ('id', 'username', 'password')
    
    def create(self, validated_data):
        user = AuthUser.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user