from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from FriendZoneApp.models import UserProfileModel, Hobby
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def index(request):
    user = request.user
    userProfile = UserProfileModel.objects.get(user = user)

    similarUsers = [] 

    context = {
        'loggedInUser' : user,
        'userProfile' : userProfile 
    }
    return render(request, 'FriendZoneApp/index.html', context)

@csrf_exempt #need to get rid of this !!!
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

#def index(request):
#    loggedInUser = UserProfileModel.objects.get(id = request.user.id) // get the user that is logged in
#    loggedInUsersHobbies = loggedInUser.hobby // get logged in users all hobbies // .hobby is from class UserProfileModel
#    otherUsers = UserProfileModel.objects.exclude(id=request.user.id) // get all users except the logged in one
#    
#    similarUsers = []  // create empty array

#    for otherUser in otherUsers:
#       counter=0
#       for h in otherUser.hobby:
#           if otherUser.hobby in loggedInUserHobbies:
#               counter++ // increment each time a user with same hobbie is found, but reset counter when new user checked
#       similarUsers.append(otherUser) // user has same hobby(ies) as logged in user so we add it to list

#    sortedUsers = function // function to sort list of users, ordering by number of similar hobbies as loggedin user

#    context = {
#        'members' : sortedUsers // users will be displayed in the order in the index.html
#    }
#    return render(request, 'FriendZoneApp/index.html', context)