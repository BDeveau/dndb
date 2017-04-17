from django.contrib import admin

from .models import Location, Character, Campaign, Task, PartyLoot

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    filter_horizontal = ["users"]

# Register your models here.
admin.site.register(Location)
admin.site.register(Character)
admin.site.register(Task)
admin.site.register(PartyLoot)
