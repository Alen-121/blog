from django.db import models
from user_auth.models import UserData
# Create your models here.
class BlogData(models.Model):
    title=models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey(UserData,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title