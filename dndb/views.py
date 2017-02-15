from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .models import Location, Character, Campaign

# Create your views here.
def index(request):
    return render(request, 'index.html')

def campaigns(request):
    return render(request, 'campaigns.html', {
        'campaigns': Campaign.objects.all
    })

def locations(request, campaign_id):
    return render(request, 'locations.html', {
        'locations': Location.objects.filter(campaign=campaign_id)
    })

def characters(request, campaign_id):
    return render(request, 'characters.html', {
        'characters': Character.objects.filter(campaign=campaign_id)
    })