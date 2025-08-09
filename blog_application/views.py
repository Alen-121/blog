from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import BlogForm
from django.views import View
from.models import BlogData
from user_auth.models import UserData
# Create your views here.
class Home(View):

    def get(self,request):
        blog_form = BlogForm()
        blog= BlogData.objects.all().order_by('-created_at')
        context ={
            'blog_form':blog_form,
            'blogs':blog,
        }
        return render(request,'home.html',context)

    def post(self,request):
        blog_form = BlogForm(request.POST)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.author= request.user
            blog.save()
            return redirect('home')
        else:
            blogs = BlogData.objects.all().order_by('-created_at')
            context = {
                'blog_form': blog_form,
                'blogs': blogs,
            }
            return render(request, 'home.html', context)
class UpdateBlog(View):
    def get(self,request,blog_id):
        if not request.user.is_authenticated:
            return redirect('login')
        blog = get_object_or_404(BlogData,id=blog_id,author=request.user)
        blog_form = BlogForm(instance=blog)
        return render(request,'update.html',{'blog_form': blog_form, 'blog': blog})
    def post(self,request,blog_id):
        if not request.user.is_authenticated:
            return redirect('login')
        blog = get_object_or_404(BlogData,id=blog_id,author=request.user)
        blog_form = BlogForm(request.POST,instance=blog)
        if blog_form.is_valid():
            update_blog = blog_form.save(commit=False)
            update_blog.author = request.user
            update_blog.save()
            return redirect('home')
        return render(request,'update.html',{'blog_form': blog_form, 'blog': blog})


class DeleteBlog(View):
    def get(self, request, blog_id):
        if not request.user.is_authenticated:
            return redirect('login')
        
        blog = get_object_or_404(BlogData, id=blog_id, author=request.user)
        return render(request, 'delete_blog.html', {'blog': blog})
    
    def post(self, request, blog_id):
        if not request.user.is_authenticated:
            return redirect('login')
        
        blog = get_object_or_404(BlogData, id=blog_id, author=request.user)
        blog.delete()
        return redirect('home')