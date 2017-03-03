from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

""" 
TODO:
Quests
Party Loot

"""

class Campaign(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='campaigns')
    
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=50)
    notes = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, related_name='locations', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
        
    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in Location.objects.filter(parent=self):
            _r = c.get_all_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r
    
class Character(models.Model):
    name = models.CharField(max_length=50)
    race = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, related_name='characters', on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, related_name='characters', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Task(models.Model):
    name = models.CharField(max_length=50)
    giver = models.ForeignKey(Character, null=True, blank=True, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, blank=True, related_name='tasks', on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, related_name='tasks', on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class PartyLoot(models.Model):
    campaign = models.ForeignKey(Campaign, related_name='partyloot', on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.campaign.name