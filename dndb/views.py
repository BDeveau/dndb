from __future__ import print_function
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.urlresolvers import reverse_lazy, reverse
from django import forms
from django.forms import inlineformset_factory
from .models import Location, Character, Campaign, Task, Item, Post, Comment, User
from .forms import LocationForm, CharacterForm, TaskForm, UserForm, ItemForm, PostForm, CommentForm, SignupForm
import sys
import requests
import urllib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from django.contrib.admin.widgets import FilteredSelectMultiple


# Create your views here.
def index(request):
    getCommits = requests.get('https://api.github.com/repos/BDeveau/dndb/commits')
    getIssues = requests.get('https://api.github.com/repos/BDeveau/dndb/issues')

    issues = getIssues.json()[:10] if getIssues.status_code == 200 else [
        {"message": "Data Not Available"},
        {"message": getIssues.reason}
    ]
    commits = getCommits.json()[:10] if getCommits.status_code == 200 else [
        {"title": "Data Not Available"},
        {"message": getIssues.reason}
    ]

    return render(request, 'index.html', {
        'issues': issues,
        'commits': commits
    })


class campaigns(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Campaign.objects.filter(users=self.request.user)


class campaign_create(LoginRequiredMixin, CreateView):
    model = Campaign
    fields = ['name']

    def form_valid(self, form):
        campaign = form.save(commit=False)
        campaign.owner = self.request.user
        campaign.save()
        campaign.users.add(self.request.user)
        campaign.save()
        self.request.session['campaign'] = campaign.name
        self.request.session['campaign_id'] = campaign.id
        return redirect('overview', campaign_id=campaign.id)


class campaign_invite(LoginRequiredMixin, UpdateView):
    model = Campaign
    fields = ['users']

    def get_success_url(self):
        return reverse('overview', kwargs={'campaign_id': self.object.id})


@login_required
def overview(request, campaign_id):
    return render(request, 'dndb/overview.html', {
        'campaign': Campaign.objects.get(id=campaign_id),
        'recent_locations': Location.objects.filter(campaign=campaign_id).order_by('-modified')[:5],
        'recent_characters': Character.objects.filter(campaign=campaign_id).order_by('-modified')[:5],
        'recent_tasks': Task.objects.filter(campaign=campaign_id, completed=False).order_by('-modified')[:5],
        'recent_items': Item.objects.filter(campaign=campaign_id).order_by('-modified')[:5],
        'recent_posts': Post.objects.filter(campaign=campaign_id).order_by('-created')[:10],
    })


@login_required
def locations(request, campaign_id):
    return render(request, 'dndb/locations.html', {
        'locations': Location.objects.filter(campaign=campaign_id)
    })


@login_required
def tasks(request, campaign_id):
    return render(request, 'dndb/tasks.html', {
        'tasks': Task.objects.filter(campaign=campaign_id)
    })


@login_required
def items(request, campaign_id):
    return render(request, 'dndb/item_list.html', {
        'items': Item.objects.filter(campaign=campaign_id)
    })


@login_required
def characters(request, campaign_id):
    return render(request, 'dndb/characters.html', {
        'characters': Character.objects.filter(campaign=campaign_id)
    })


@login_required
def character_detail(request, **kwargs):
    if 'character_id' in kwargs:
        character = Character.objects.get(id=kwargs['character_id'])
    else:
        character = Character.objects.filter(name__icontains=urllib.unquote(kwargs['character_name'])).first()

    form = CharacterForm(instance=character)
    form.fields['location'].queryset = Location.objects.filter(
        campaign=request.session['campaign_id'])

    if request.method == "POST":
        form = CharacterForm(request.POST, instance=character)
        if 'delete' in request.POST:
            character.delete()
            messages.warning(request, 'Character DELETED.')
            return redirect('characters', campaign_id=request.session['campaign_id'])
        if form.is_valid():
            post = form.save(commit=False)
            # more stuff if needed
            post.save()
            messages.success(request, 'Character Updated.')
            return redirect('character', character_id=character.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/character_detail.html', {
        'form': form,
        'character': character,
        'tasks': Task.objects.filter(giver=character.id),
    })


@login_required
def character_create(request, **kwargs):
    form = CharacterForm()
    form.fields['location'].queryset = Location.objects.filter(
        campaign=request.session['campaign_id'])

    if 'location_id' in kwargs:
        form.fields['location'].initial = kwargs['location_id']

    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.campaign = Campaign.objects.get(
                id=request.session['campaign_id'])
            post.save()
            messages.success(request, 'New Character Created.')
            return redirect('character', character_id=post.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/character_detail.html', {
        'form': form
    })


@login_required
def location_detail(request, **kwargs):
    if 'location_id' in kwargs:
        location = Location.objects.get(id=kwargs['location_id'])
    else:
        location = Location.objects.filter(name__icontains=urllib.unquote(kwargs['location_name'])).first()

    form = LocationForm(instance=location)
    form.fields['parent'].queryset = Location.objects.filter(
        campaign=request.session['campaign_id'])

    if request.method == "POST":
        if 'delete' in request.POST:
            location.delete()
            messages.warning(request, 'Location DELETED.')
            return redirect('locations', campaign_id=request.session['campaign_id'])
        if form.is_valid():
            post = form.save(commit=False)
            # more stuff if needed
            post.save()
            messages.success(request, 'Location Updated.')
            return redirect('location', location_id=location.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/location_detail.html', {
        'form': form,
        'location': location,
        'characters': location.get_all_children_characters(),
        'tasks': location.get_all_children_tasks(),
        'children': location.get_all_children(),
    })


@login_required
def location_create(request, **kwargs):
    form = LocationForm()
    form.fields['parent'].queryset = Location.objects.filter(
        campaign=request.session['campaign_id'])

    if 'parent_id' in kwargs:
        form.fields['parent'].initial = kwargs['parent_id']

    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.campaign = Campaign.objects.get(
                id=request.session['campaign_id'])
            post.save()
            messages.success(request, 'New Location Created.')
            return redirect('location', location_id=post.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/location_detail.html', {
        'form': form
    })


@login_required
def task_detail(request, **kwargs):
    if 'task_id' in kwargs:
        task = Task.objects.get(id=kwargs['task_id'])
    else:
        task = Task.objects.filter(name__icontains=urllib.unquote(kwargs['task_name'])).first()

    form = TaskForm(instance=task)
    form.fields['giver'].queryset = Character.objects.filter(
        campaign=request.session['campaign_id'])
    form.fields['location'].queryset = Location.objects.filter(
        campaign=request.session['campaign_id'])

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if 'delete' in request.POST:
            task.delete()
            messages.warning(request, 'Task DELETED.')
            return redirect('tasks', campaign_id=request.session['campaign_id'])
        if form.is_valid():
            post = form.save(commit=False)
            # more stuff if needed
            post.save()
            messages.success(request, 'Task Updated.')
            return redirect('task', task_id=task.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/task_detail.html', {
        'form': form,
        'task': task
    })


@login_required
def task_create(request, **kwargs):
    form = TaskForm()
    form.fields['giver'].queryset = Character.objects.filter(
        campaign=request.session['campaign_id'])
    form.fields['location'].queryset = Location.objects.filter(
        campaign=request.session['campaign_id'])

    if 'location_id' in kwargs:
        form.fields['location'].initial = kwargs['location_id']

    if 'character_id' in kwargs:
        form.fields['giver'].initial = kwargs['character_id']

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.campaign = Campaign.objects.get(
                id=request.session['campaign_id'])
            post.save()
            messages.success(request, 'New Task Created.')
            return redirect('task', task_id=post.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/task_detail.html', {
        'form': form
    })


@login_required
def item_detail(request, **kwargs):
    if 'item_id' in kwargs:
        item = Item.objects.get(id=kwargs['item_id'])
    else:
        item = Item.objects.filter(name__icontains=urllib.unquote(kwargs['item_name'])).first()

    form = ItemForm(instance=item)

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if 'delete' in request.POST:
            item.delete()
            messages.warning(request, 'Item DELETED.')
            return redirect('items', campaign_id=request.session['campaign_id'])
        if form.is_valid():
            post = form.save(commit=False)
            # more stuff if needed
            post.campaign_id = request.session['campaign_id']
            post.save()
            messages.success(request, 'Item Updated.')
            return redirect('item_detail', item_id=post.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/item_detail.html', {
        'form': form,
        'item': item
    })


@login_required
def item_create(request, **kwargs):
    form = ItemForm()

    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.campaign = Campaign.objects.get(
                id=request.session['campaign_id'])
            post.save()
            messages.success(request, 'New Item Created.')
            return redirect('item_detail', item_id=post.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/item_detail.html', {
        'form': form
    })


@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            # more stuff if needed
            p.author = request.user
            p.post = post
            p.save()
            messages.success(request, 'Comment Posted.')
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/post_detail.html', {
        'edit': False,
        'form': form,
        'post': post
    })


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if 'delete' in request.POST:
            post.delete()
            messages.warning(request, 'Post DELETED.')
            return redirect('overview', campaign_id=request.session['campaign_id'])
        if form.is_valid():
            p = form.save(commit=False)
            # more stuff if needed
            p.save()
            messages.success(request, 'Post Updated.')
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/post_detail.html', {
        'edit': True,
        'form': form,
        'post': post
    })


@login_required
def post_create(request, **kwargs):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.campaign = Campaign.objects.get(
                id=request.session['campaign_id'])
            p.author = request.user
            p.save()
            messages.success(request, 'New Post Created.')
            return redirect('post_detail', post_id=p.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/post_detail.html', {
        'edit': True,
        'form': form
    })


@login_required
def comment_detail(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    form = CommentForm(instance=comment)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if 'delete' in request.POST:
            comment.delete()
            messages.warning(request, 'Comment DELETED.')
            return redirect('overview', campaign_id=request.session['campaign_id'])
        if form.is_valid():
            p = form.save(commit=False)
            # more stuff if needed
            p.save()
            messages.success(request, 'Comment Updated.')
            return redirect('comment_detail', comment_id=comment.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/comment_detail.html', {
        'form': form,
        'comment': comment
    })


@login_required
def comment_create(request, **kwargs):
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.campaign = Campaign.objects.get(
                id=request.session['campaign_id'])
            p.author = request.user
            p.save()
            messages.success(request, 'New Comment Created.')
            return redirect('comment_detail', post_id=p.id)
        else:
            messages.error(request, form.errors)

    return render(request, 'dndb/comment_detail.html', {
        'form': form
    })


@login_required
def user_detail(request):
    user = User.objects.get(id=request.user.id)
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User Registered.')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
            messages.error(request, form.non_field_errors)

    return render(request, 'dndb/user_detail.html', {
        'form': form
    })


class register_user(CreateView):
    model = User
    form_class = SignupForm

    def form_valid(self, form):
        # save the new user first
        u = form.save(commit=False)
        u.set_password(self.request.POST.get('password'))
        u.save()
        # get the username and password
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        # authenticate user then login
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return redirect('profile')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'dndb/change_password.html', {
        'form': form
    })


@login_required
def selectcampaign(request, campaign_id):
    c = Campaign.objects.get(pk=campaign_id)
    request.session['campaign'] = c.name
    request.session['campaign_id'] = c.id
    return redirect("/campaign/" + str(c.id))


@login_required
def join_campaign(request):
    return redirect("overview")


@login_required
def create_join_link(request, campaign_id):
    c = Campaign.objects.get(pk=campaign_id)
    return redirect("overview")
