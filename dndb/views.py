from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Location, Character, Campaign

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html', {
    })
    
@login_required
def campaigns(request):
    return render(request, 'dndb/campaigns.html', {
        'campaigns': Campaign.objects.filter(users=request.user)
    })
    
@login_required
def locations(request, campaign_id):
    return render(request, 'dndb/locations.html', {
        'locations': Location.objects.filter(campaign=campaign_id)
    })
    
@login_required
def characters(request, campaign_id):
    return render(request, 'dndb/characters.html', {
        'characters': Character.objects.filter(campaign=campaign_id)
    })
    
@login_required
def selectcampaign(request, campaign_id):
    c = Campaign.objects.get(pk=campaign_id)
    request.session['campaign'] = c.name
    request.session['campaign_id'] = c.id
    return redirect("/campaign/" + str(c.id) + "/characters/")