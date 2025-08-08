from django.contrib.auth.models import User
from django import forms
from .models import UserData


class UserSignUp(forms.ModelForm):
    password = forms.CharField(max_length=12,min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    repassword = forms.CharField(max_length=12,min_length=8, widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    
    
    class Meta:
        model=UserData
        fields=['username','first_name','last_name']
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        print(f"Password from cleaned_data: {password}")  # Debug line
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class UserLogin(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=12,min_length=8,widget=forms.PasswordInput())

