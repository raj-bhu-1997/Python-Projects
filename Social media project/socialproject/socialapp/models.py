from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
  #author = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, default = None)
  title = models.CharField(max_length= 30, blank=True, null= True)
  text = models.TextField()
  created_on = models.DateTimeField(default = timezone.now)
  image = models.ImageField(upload_to = 'upload/post_photos', default = None, null= True, blank= True)
  likes = models.ManyToManyField(User, blank=True, related_name='likes')
  dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
  

class Comment(models.Model):
  comments = models.TextField()
  author = models.ForeignKey(User, on_delete = models.CASCADE)
  post = models.ForeignKey(Post, on_delete = models.CASCADE)
  created_on = models.DateTimeField(default=timezone.now)
  like = models.ManyToManyField(User, blank = True, related_name='like')
  dislike = models.ManyToManyField(User, blank = True, related_name='dislike')
    
  
class Profile(models.Model):
  user = models.OneToOneField(User, verbose_name = 'user',null= True, related_name = 'profile', on_delete = models.CASCADE)
  name = models.CharField(max_length= 30, blank=True, null = True)
  bio = models.TextField(blank=True, null=True)
  date_of_birth = models.DateField(blank=True, null=True)
  location = models.CharField(max_length=30, blank=True, null= True)
  image = models.ImageField(upload_to = 'upload/profile_photos', default = 'upload/profile_photos/default.jpg', null= True)
  followers = models.ManyToManyField(User, blank= True, related_name= 'following')
  
@receiver(post_save, sender= User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user= instance)
    print('user profile created')

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()