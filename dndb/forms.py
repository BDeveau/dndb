from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from dndb.models import Character, Location, Task, PartyLoot, Campaign


class CharacterForm(ModelForm):

    class Meta:
        model = Character
        fields = ['name', 'race', 'sex', 'title', 'location', 'notes']


class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ['name', 'parent', 'notes']


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'giver', 'location', 'completed', 'notes']


class PartyLootForm(ModelForm):

    class Meta:
        model = PartyLoot
        fields = ['items', 'notes']


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
