from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import Location, Character, Campaign, Task, PartyLoot
from .forms import LocationForm, CharacterForm, TaskForm, PartyLootForm, UserForm
import sys

# Create your views here.
def index(request):
    return render(request, 'index.html', {
    })
    
@login_required
def campaigns(request):
    return render(request, 'dndb/campaigns.html', {
        'campaigns': Campaign.objects.filter(users=request.user)
    })

@login_required
def overview(request, campaign_id):
    return render(request, 'dndb/overview.html', {
        'recent_locations': Location.objects.filter(campaign=campaign_id).order_by('-modified')[:5],
        'recent_characters': Character.objects.filter(campaign=campaign_id).order_by('-modified')[:5],
        'recent_tasks': Task.objects.filter(campaign=campaign_id).order_by('-modified')[:5],
        'partyloot': PartyLoot.objects.filter(campaign=campaign_id).first(),
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
def characters(request, campaign_id):
    return render(request, 'dndb/characters.html', {
        'characters': Character.objects.filter(campaign=campaign_id)
    })

@login_required
def character_detail(request, character_id):
    
    character = Character.objects.get(id=character_id)
    form = CharacterForm(instance=character)
    form.fields['location'].queryset = Location.objects.filter(campaign=request.session['campaign_id'])

    if request.method == "POST":
        form = CharacterForm(request.POST, instance=character)
        if form.is_valid():
            post = form.save(commit=False)
            #more stuff if needed
            post.save()
            messages.success(request, 'Character Updated.')
            return redirect('character', character_id=character.id)

    return render(request, 'dndb/character_detail.html', {
        'form': form,
        'character': character,
        'tasks': Task.objects.filter(giver=character_id),
    })
    
@login_required
def character_create(request, **kwargs):
    
    form = CharacterForm()
    form.fields['location'].queryset = Location.objects.filter(campaign=request.session['campaign_id'])
    
    if 'location_id' in kwargs:
        form.fields['location'].initial = kwargs['location_id']
    
    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.campaign = Campaign.objects.get(id=request.session['campaign_id'])
            post.save()
            messages.success(request, 'New Character Created.')
            return redirect('character', character_id=post.id)
            
    return render(request, 'dndb/character_detail.html', {
        'form': form
    })

@login_required
def location_detail(request, location_id):
    
    location = Location.objects.get(id=location_id)
    form = LocationForm(instance=location)
    form.fields['parent'].queryset = Location.objects.filter(campaign=request.session['campaign_id'])
    
    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            post = form.save(commit=False)
            #more stuff if needed
            post.save()
            messages.success(request, 'Location Updated.')
            return redirect('location', location_id=location.id)
    
    return render(request, 'dndb/location_detail.html', {
        'form': form,
        'location': location,
        'characters': Character.objects.filter(location=location_id),
        'tasks': Task.objects.filter(location=location_id),
        'children': location.get_all_children(),
    })
    
@login_required
def location_create(request, **kwargs):
    
    form = LocationForm()
    form.fields['parent'].queryset = Location.objects.filter(campaign=request.session['campaign_id'])
    
    if 'parent_id' in kwargs:
        form.fields['parent'].initial = kwargs['parent_id']
    
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.campaign = Campaign.objects.get(id=request.session['campaign_id'])
            post.save()
            messages.success(request, 'New Location Created.')
            return redirect('location', location_id=post.id) 
          
    return render(request, 'dndb/location_detail.html', {
        'form': form
    })
    
@login_required
def task_detail(request, task_id):
    
    task = Task.objects.get(id=task_id)
    form = TaskForm(instance=task)
    form.fields['giver'].queryset = Character.objects.filter(campaign=request.session['campaign_id'])
    form.fields['location'].queryset = Location.objects.filter(campaign=request.session['campaign_id'])
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            post = form.save(commit=False)
            #more stuff if needed
            post.save()
            messages.success(request, 'Task Updated.')
            return redirect('task', task_id=task.id)
            
    return render(request, 'dndb/task_detail.html', {
        'form': form,
        'task': task
    })
    
@login_required
def task_create(request, **kwargs):
    
    form = TaskForm()
    form.fields['giver'].queryset = Character.objects.filter(campaign=request.session['campaign_id'])
    form.fields['location'].queryset = Location.objects.filter(campaign=request.session['campaign_id'])
    
    if 'location_id' in kwargs:
        form.fields['location'].initial = kwargs['location_id']
        
    if 'character_id' in kwargs:
        form.fields['giver'].initial = kwargs['character_id']
    
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.campaign = Campaign.objects.get(id=request.session['campaign_id'])
            post.save()
            messages.success(request, 'New Task Created.')
            return redirect('task', task_id=post.id)
            
    return render(request, 'dndb/task_detail.html', {
        'form': form
    })
    
@login_required
def partyloot_detail(request, campaign_id):
    
    loot = PartyLoot.objects.filter(campaign=campaign_id).first()
    form = PartyLootForm(instance=loot)
    
    if request.method == "POST":
        form = PartyLootForm(request.POST, instance=loot)
        if form.is_valid():
            post = form.save(commit=False)
            #more stuff if needed
            post.save()
            messages.success(request, 'Partyloot Updated.')
            return redirect('partyloot', campaign_id)
            
    if not loot:
        return redirect('partyloot_create')    
         
    return render(request, 'dndb/partyloot_detail.html', {
        'form': form,
        'campaign': Campaign.objects.get(id=campaign_id)
    })

@login_required
def partyloot_create(request):
    
    form = PartyLootForm()
    
    if request.method == "POST":
        form = PartyLootForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.campaign = Campaign.objects.get(id=request.session['campaign_id'])
            post.save()
            messages.success(request, 'Partyloot Created.')
            return redirect('partyloot', campaign_id=post.campaign.id)
            
    return render(request, 'dndb/partyloot_detail.html', {
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
            messages.success(request, 'Profile Updated.')
            return redirect('profile')
         
    return render(request, 'dndb/user_detail.html', {
        'form': form
    })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
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