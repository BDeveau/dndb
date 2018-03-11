from django.forms import ModelForm
from django import forms
from dndb.models import Character, Location, Task, PartyLoot, Campaign, Item, Post, Comment, User


class CharacterForm(ModelForm):

    class Meta:
        model = Character
        fields = ['name', 'race', 'sex', 'title', 'location', 'notes']


class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ['name', 'location_type', 'parent', 'notes']


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'giver', 'location', 'completed', 'notes']


class ItemForm(ModelForm):

    class Meta:
        model = Item
        fields = ['name', 'quantity', 'notes']


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body']
        help_texts = {
            'body': 'You can create links by specifying what you\'re typing in brackets. For example'
                    ' you can type: [character]Jonny[/character] or [location]Tavern[/location]',
        }


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['body']
