from django.contrib import admin

from .models import Location, Character, Campaign, Task, PartyLoot, Item, Post, Comment

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    filter_horizontal = ["users"]

# Register your models here.
admin.site.register(Location)
admin.site.register(Character)
admin.site.register(Task)
admin.site.register(PartyLoot)
admin.site.register(Item)
admin.site.register(Post)
admin.site.register(Comment)
