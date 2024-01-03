from django.db import models
from account.models import User
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    post = models.FileField()
    title = models.CharField(max_length = 200,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'post')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Liked by {self.user.username} on post {self.post.id}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.user.username} on post {self.post.id}'

    
