from django.shortcuts import render

# Create your views here.

def index(request):
    context = {"pageTitle": "FriendZone"}
    return render (request, 'index.html', context)
