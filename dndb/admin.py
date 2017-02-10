from django.contrib import admin

from .models import Location, Character, Campaign

# Register your models here.
admin.site.register(Location)
admin.site.register(Character)
admin.site.register(Campaign)