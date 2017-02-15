from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Location, Character, Campaign

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html', {
        'campaigns': Campaign.objects.filter(users=request.user)
    })
    
@login_required
def campaigns(request):
    return render(request, 'campaigns.html', {
        'campaigns': Campaign.objects.filter(users=request.user)
    })
    
@login_required
def locations(request, campaign_id):
    return render(request, 'locations.html', {
        'locations': Location.objects.filter(campaign=campaign_id)
    })
    
@login_required
def characters(request, campaign_id):
    return render(request, 'characters.html', {
        'characters': Character.objects.filter(campaign=campaign_id)
    })
    
@login_required
def selectcampaign(request):
    request.session['campaign'] = request.POST['campaignselect']
    return True