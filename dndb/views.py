from django.shortcuts import render
from django.http import HttpResponse

from .models import Location, Character

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def locations(request):
    return render(request, 'locations.html', {
        'locations': Location.objects.all()
    })
    
def characters(request):
    return render(request, 'characters.html', {
        'characters': Character.objects.all()
    })