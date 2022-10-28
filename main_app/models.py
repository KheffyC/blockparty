from django.urls import reverse
from django.db import models
# from django.urls import reverse

from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=2)
    # add pfp later

class GlobalPost(models.Model):
    content = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.content} made by {self.user}"
    
    def get_absolute_url(self):
        return reverse("global_index")
    
    class Meta:
        ordering = ['-date']
    
class Comment(models.Model):
    content = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(GlobalPost, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.content} made by {self.user}"