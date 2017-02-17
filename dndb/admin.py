from django.contrib import admin

from .models import Location, Character, Campaign, Task, PartyLoot

# Register your models here.
admin.site.register(Location)
admin.site.register(Character)
admin.site.register(Campaign)
admin.site.register(Task)
admin.site.register(PartyLoot)