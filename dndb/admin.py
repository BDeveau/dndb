from django.contrib import admin
from .models import User, Location, Character, Campaign, Task, Item, Post, Comment

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    filter_horizontal = ["users"]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ["date_joined"]
    list_display = ["email", "username"]
    search_fields = ["email", "username"]

# Register your models here.
admin.site.register(Location)
admin.site.register(Character)
admin.site.register(Task)
admin.site.register(Item)
admin.site.register(Post)
admin.site.register(Comment)
