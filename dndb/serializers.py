from rest_framework import serializers
from dndb.models import Campaign, Character, Location, Task, PartyLoot
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = ['name', 'owner', 'users', 'locations', 'characters']


class CharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = ['name', 'race', 'sex', 'title', 'location',
                  'notes', 'created', 'modified', 'campaign']


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['name', 'parent', 'notes', 'created', 'modified', 'campaign']


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['name', 'giver', 'location',
                  'notes', 'created', 'modified', 'campaign']


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['name', 'quantity', 'notes']


class PartyLootSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartyLoot
        fields = '__all__'
