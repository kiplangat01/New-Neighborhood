from django.db import models
from django.contrib.auth.models import User 
from cloudinary.models import CloudinaryField

class NeighbourHood(models.Model):
    name = models.CharField(max_length=200)
    location =  models.CharField(max_length=200)
    photo = CloudinaryField('image')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=300, blank=True, null=True)
    photo = CloudinaryField('image', blank = True)
    neighborhood = models.ForeignKey(NeighbourHood, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Updates(models.Model):
    display = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, blank=True, null=True)
    body = models.TextField()
    neighborhood = models.ForeignKey(NeighbourHood, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.title

class Business(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, blank=True, null=True)
    location = models.TextField()
    contact = models.CharField(max_length=300, blank=True, null=True)
    neighborhood = models.ForeignKey(NeighbourHood, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.name
