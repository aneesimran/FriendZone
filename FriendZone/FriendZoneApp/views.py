from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from FriendZoneApp.models import UserProfileModel, Hobby
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from FriendZoneApp.forms import EditProfileForm, RegisterProfileForm
# Create your views here.


def index(request):
    user = request.user
    userProfile = UserProfileModel.objects.get(user = user)
    userHobbies = userProfile.hobby
    otherUserProfiles = UserProfileModel.objects.exclude(user = request.user)
    similarUsers = []

    for a in otherUserProfiles:
        theirHobbies = a.hobby
        for aH in theirHobbies.all():
            for uH in userHobbies.all():
                if aH==uH:
                    similarUsers.append(a)

    def sortUsers(copySimUsers, userHobbies):
        global highest
        global mostSimilar
        index = 0;
        for copysimuser in copySimUsers:
            for copysimuserhobby in copysimuser.hobby.all():
                counter = 0
                for userhobby in userHobbies.all():
                    if copysimuserhobby == userhobby:
                        counter = counter + 1

            if counter > highest:
                highest = counter
                mostSimilar = copysimuser
        sortedSimUsers.append(mostSimilar)
        try:
            copySimUsers.remove(mostSimilar)
        except:
            print("Error")
        return copySimUsers

    copySimUsers = similarUsers[:]
    mostSimilar = copySimUsers[0]
    for userss in copySimUsers:
        copySimUsers = sortUsers(copySimUsers, userHobbies)

    for z in sortedSimUsers:
        print("HUUKEH")
        print(z)

    context = {
        'loggedInUser' : user,
        'userProfile' : userProfile,
        'similarUsers' : similarUsers,
        'oUP' : otherUserProfiles
    }
    return render(request, 'FriendZoneApp/index.html', context)



@csrf_exempt #need to get rid of this !!!
def register(request):
    if request.method == 'POST':
        form = RegisterProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfileModel.objects.create(user = user)
            login(request, user)
            #log user in !
            return redirect('/index/')
    else:
        form = RegisterProfileForm()
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
    userProfile = UserProfileModel.objects.get(user = request.user)

    context = {
        'userProfile' : userProfile
    }
    return render(request, 'FriendZoneApp/profile.html', context)

def editprofile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance = UserProfileModel.objects.get(user = request.user))

        if form.is_valid():
            form.save()
            return redirect('/profile/')

    else:
        form = EditProfileForm(instance = UserProfileModel.objects.get(user = request.user))
        args = {'form': form}
        return render(request, 'FriendZoneApp/editprofile.html', args)

def forgotpassword_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user = request.user)

        if form.is_valid():
            form.save()

            return redirect('/login/')
        else:
            return redirect('/password/')
    else:
        form = PasswordChangeForm(user = request.user)

        args = {'form': form}
        return render(request, 'FriendZoneApp/password.html', args)









#def index(request):
 #   loggedInUser = UserProfileModel.objects.get(id = request.user.id)  // get the user that is logged in
  #  loggedInUserHobbies = loggedInUser.hobby // get logged in users all hobbies // .hobby is from class UserProfileModel
   # otherUsers = UserProfileModel.objects.exclude(id = request.user.id)  //get all users except the logged in one

    #similarUsers = [] // create empty array

    #for otherUser in otherUsers:
     #   counter = 0
      #  for h in otherUser.hobby:
       #     if otherUser.hobby in loggedInUserHobbies:
        #        counter++ // increment each time a user with same hobby is found, but reset counter when new user is checked

        #similarUsers.append(otherUser) // user has same Hobby(ies) as logged in user so we add it to the list

    #sortedUsers = function // function to sort list of users, ordering by number of similar hobbies as loggedin user

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
    #context = {
     #   'members' : sortedUsers, // users will be displayed in the order in the index.html
    #}
    #return render(request, 'FriendZoneApp/index.html', context)
