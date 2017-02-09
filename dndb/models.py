from django.db import models

# Create your models here.

class Location(models.Model):
    location_name = models.CharField(max_length=50)
    location_text = models.TextField(blank=True)
    location_location = models.ForeignKey('self', blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.location_name
    
class Character(models.Model):
    character_name = models.CharField(max_length=50)
    character_race = models.CharField(max_length=20, blank=True)
    character_sex = models.CharField(max_length=10, blank=True)
    character_text = models.TextField(blank=True)
    character_location = models.ForeignKey(Location, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.character_name