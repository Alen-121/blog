# blog_application/api_views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import BlogData
from .serializers import BlogSerializer, BlogCreateUpdateSerializer

class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BlogData.objects.all().order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogCreateUpdateSerializer
        return BlogSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def update(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.author != request.user:
            return Response(
                {'error': 'You can only update your own blogs'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.author != request.user:
            return Response(
                {'error': 'You can only delete your own blogs'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def my_blogs(self, request):
        """Get blogs created by the current user"""
        blogs = BlogData.objects.filter(author=request.user).order_by('-created_at')
        page = self.paginate_queryset(blogs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(blogs, many=True)
        return Response(serializer.data)