from django.forms import ModelForm
from dndb.models import Character, Location

class CharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'race', 'sex', 'title', 'location', 'notes']

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'parent', 'notes']