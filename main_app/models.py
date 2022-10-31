from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

# class SubGroup(Group):
#     pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    state = models.CharField(max_length=2, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    groups = models.ManyToManyField(Group)
    

    # add pfp later
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        
       

class GlobalPost(models.Model):
    content = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

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