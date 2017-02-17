from django.contrib import admin

from .models import Location, Character, Campaign, Task

# Register your models here.
admin.site.register(Location)
admin.site.register(Character)
admin.site.register(Campaign)
admin.site.register(Task)