from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from FriendZoneApp.models import UserProfileModel
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    members = User.objects.exclude(id = request.user.id)
    context = {
        'members' : members
    }
    return render(request, 'FriendZoneApp/index.html', context)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfileModel.objects.create(user = user)
            login(request, user)
            #log user in !
            return redirect('/index/')
    else: 
        form = UserCreationForm()
    return render (request, 'FriendZoneApp/register.html', {'form': form,'pageTitle': '- Register'})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): 
            #log the user in 
            user = form.get_user()
            login(request, user)
            return redirect('/index/')
    else: 
        form = AuthenticationForm()
    return render (request, 'FriendZoneApp/login.html', {'form': form, 'pageTitle': '- Login'})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')

def profile_view(request):
    return render(request, 'FriendZoneApp/profile.html')

