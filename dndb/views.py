from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .models import Location, Character

# Create your views here.
def index(request):
    return render(request, 'index.html')

def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
    else:
        # Return an 'invalid login' error message.
        redirect('/')

def locations(request, campaign_id):
    return render(request, 'locations.html', {
        'locations': Location.objects.filter(campaign=campaign_id)
    })

def characters(request, campaign_id):
    return render(request, 'characters.html', {
        'characters': Character.objects.filter(campaign=campaign_id)
    })