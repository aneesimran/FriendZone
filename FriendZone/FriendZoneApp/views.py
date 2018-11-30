from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render (request, 'index.html', {'content': 'ghana'})

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
    return render (request, 'register.html', {'form': form})