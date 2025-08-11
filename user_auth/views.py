from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.views import View
from django.http import HttpResponse
from .forms import UserSignUp,UserLogin
from django.contrib import messages
from .models import UserData
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# Create your views here.
class UserSignUpView(View):
    def get(self,request):
        if request.user.is_authenticated:
            messages.info(request,'You are already logged in')
            return redirect('home')
        signup_form = UserSignUp()
        return render(request,'signup.html',{'signup_form':signup_form})



    def post(self,request):
        if request.user.is_authenticated:
            return redirect('home')
        user_signup = UserSignUp(request.POST)
        if user_signup.is_valid():
            user =user_signup.save()
            print('user created: ',user)
            print('user password :',user.password)
            messages.success(request,'Sucessfully registered Please Login')
            return redirect('login')
        else:
            signup_form= user_signup
            return render(request,'signup.html',{'signup_form':signup_form})

 

class UserLoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('home')

        userlogin_form= UserLogin()
        return render(request,'login.html',{'userlogin_form':userlogin_form})
    
    def post(self,request):

        if request.user.is_authenticated:
            return redirect('home')
            
        form = UserLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,'Invalid credentials')
        return render(request,'login.html',{'userlogin_form':form})

@login_required
def logout_view(request):
    user_name = request.user.get_full_name() or request.user.username
    request.session.flush()
    logout(request)
    return redirect('login')