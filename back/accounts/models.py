from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None
    user_age = models.PositiveIntegerField(null=True)
    user_introduction = models.CharField(max_length=100, blank=True)
    user_profile_img = models.ImageField(upload_to='profiles/', blank=True, default='accounts/profiles/default_profile.png')
    user_banner_img = models.ImageField(upload_to='banners/', blank=True, default='accounts/banners/default_banner.png')
    followers = models.ManyToManyField('accounts.User', related_name='followings')
