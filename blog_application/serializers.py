from rest_framework import serializers
from .models import BlogData
from user_auth.serializer import UserSerializer


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = BlogData
        fields=['id','title','description','author','created_at','updated_at']
        read_only_fields=['id','author','created_at','updated_at']

class BlogCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogData
        fields=['title','description']