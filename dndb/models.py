from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Campaign(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User)
    
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=50)
    notes = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Character(models.Model):
    name = models.CharField(max_length=50)
    race = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name