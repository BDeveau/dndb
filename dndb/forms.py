from django.forms import ModelForm
from django import forms
from dndb.models import Character, Location, Task, Campaign, Item, Post, Comment, User


class CharacterForm(ModelForm):

    class Meta:
        model = Character
        fields = ['name', 'race', 'sex', 'title', 'location', 'notes', 'gm_info']

    def __init__(self, *args, **kwargs):
        gm = kwargs.pop('gm', 0)
        super(CharacterForm, self).__init__(*args, **kwargs)
        if not gm:
            del self.fields['gm_info']


class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ['name', 'location_type', 'parent', 'notes', 'gm_info']

    def __init__(self, *args, **kwargs):
        gm = kwargs.pop('gm', 0)
        super(LocationForm, self).__init__(*args, **kwargs)
        if not gm:
            del self.fields['gm_info']


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'giver', 'location', 'completed', 'notes', 'gm_info']

    def __init__(self, *args, **kwargs):
        gm = kwargs.pop('gm', 0)
        super(TaskForm, self).__init__(*args, **kwargs)
        if not gm:
            del self.fields['gm_info']


class ItemForm(ModelForm):

    class Meta:
        model = Item
        fields = ['name', 'quantity', 'notes', 'gm_info']

    def __init__(self, *args, **kwargs):
        gm = kwargs.pop('gm', 0)
        super(ItemForm, self).__init__(*args, **kwargs)
        if not gm:
            del self.fields['gm_info']


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
