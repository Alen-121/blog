from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserData

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    repassword = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = UserData
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'repassword']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['repassword']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('repassword')
        password = validated_data.pop('password')
        user = UserData.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('Must include username and password')