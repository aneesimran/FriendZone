from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render (request, 'FriendZoneApp/index.html', {'content': 'ghana'})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #log user in !
            return redirect('/index/')
    else: 
        form = UserCreationForm()
    return render (request, 'FriendZoneApp/register.html', {'form': form})

#@csrf_exempt
#def login_view(request):
#    if request.method == 'POST':
#        #do something
#    else: 
#        form = AuthenticationForm()
#    return render (request, 'FriendZoneApp/login.html', {'form': form})