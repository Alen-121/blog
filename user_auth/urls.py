from django.urls import path
from .views import UserSignUpView,UserLoginView,logout_view


urlpatterns=[
    path('signup/',UserSignUpView.as_view(),name='signup'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/', logout_view, name='logout'),
]