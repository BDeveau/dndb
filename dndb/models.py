from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import gettext as _
from django.core import validators
import sys


class User(AbstractBaseUser, PermissionsMixin):
    """
    A class implementing a fully featured User model with admin-compliant
    permissions.

    Email and password are required. Other fields are optional.
    """

    first_name = models.CharField(max_length=50, blank=True)

    last_name = models.CharField(max_length=50, blank=True)

    email = models.EmailField(
        _('Email Address'), unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    username = models.CharField(
        _('Username'), max_length=30, unique=True, blank=True, null=True,
        help_text=_('30 characters or fewer. Letters, numbers and _ only.'),
        validators=[
            validators.RegexValidator(
                r'^\w+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers and _ character.'),
                'invalid'
            ),
        ],
        error_messages={
            'unique': _("The username is already taken."),
        }
    )
    is_staff = models.BooleanField(
        _('Staff Status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.')
    )
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta(object):
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = False

    def get_full_name(self):
        """
        Returns the fullname for the user.
        """
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Campaign(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='campaigns')
    owner = models.ForeignKey(
        User, related_name='owned_campaigns', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    notes = models.TextField(null=True, blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    campaign = models.ForeignKey(
        Campaign, related_name='locations', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    location_type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_all_children(self):
        r = []
        r.extend(self.children.all())
        for c in Location.objects.filter(parent=self):
            r.extend(c.get_all_children())
        return r

    def get_all_children_characters(self):
        r = []
        r.extend(self.characters.all())
        for c in Location.objects.filter(parent=self):
            r.extend(c.get_all_children_characters())
        return r

    def get_all_children_tasks(self):
        r = []
        r.extend(self.tasks.all())
        for c in Location.objects.filter(parent=self):
            r.extend(c.get_all_children_tasks())
        return r


class Character(models.Model):
    name = models.CharField(max_length=50)
    race = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    location = models.ForeignKey(
        Location, null=True, blank=True, related_name='characters', on_delete=models.CASCADE)
    campaign = models.ForeignKey(
        Campaign, related_name='characters', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=50)
    giver = models.ForeignKey(Character, null=True,
                              blank=True, on_delete=models.CASCADE)
    location = models.ForeignKey(
        Location, null=True, blank=True, related_name='tasks', on_delete=models.CASCADE)
    campaign = models.ForeignKey(
        Campaign, related_name='tasks', on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    campaign = models.ForeignKey(
        Campaign, related_name='items', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PartyLoot(models.Model):
    campaign = models.ForeignKey(
        Campaign, related_name='partyloot', on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.campaign.name


class Post(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    campaign = models.ForeignKey(
        Campaign, related_name='posts', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    body = models.TextField(null=False, blank=False)
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
