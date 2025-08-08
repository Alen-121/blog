from django.urls import path
from .views import Home,UpdateBlog,DeleteBlog


urlpatterns=[
    path('',Home.as_view(),name='home'),
    path('update/<int:blog_id>',UpdateBlog.as_view(),name='update'),
    path('delete/<int:blog_id>',DeleteBlog.as_view(),name='delete'),
]