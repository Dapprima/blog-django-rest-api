from django.db import models
from django.contrib.auth.models import User


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_request = models.DateTimeField()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=250)
    body = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)    
    

class Unlike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='unlikes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)