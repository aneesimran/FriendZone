from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from FriendZoneApp.models import UserProfileModel, Hobby
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from FriendZoneApp.forms import EditProfileForm, RegisterForm
from datetime import date
from django.core import serializers
from django.core.mail import send_mail
import operator

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

    sortedUsers = []
    copySimUsers = similarUsers[:]

    for sUser in copySimUsers: 
        temp = {
            0: sUser.id,
            1: sUser.first_name, 
            2: sUser.last_name, 
            3: sUser.hobby.all(),
            'count': sUser.hobby.all().count()
        }
        print(temp[2])
        sortedUsers.append(temp)

    print(sortedUsers)
    sortedUsers.sort(key=operator.itemgetter('count'), reverse = True)
    print("")
    print(sortedUsers)

    context = {
        'loggedInUser' : user,
        'userProfile' : userProfile,
        'similarUsers' : similarUsers,
        'oUP' : otherUserProfiles,
        'sortedUsers': sortedUsers
    }
    return render(request, 'FriendZoneApp/index.html', context)



def filterUsers(request):
    print("GHANA filerUsers accedded GHANA")
    gender = request.GET['gender']
    ageFilter = request.GET['chosenAge']

    user = request.user
    userProfile = UserProfileModel.objects.get(user = user)
    print(userProfile.hobby.all)
    userHobbies = userProfile.hobby
    otherUserProfiles = UserProfileModel.objects.exclude(user = request.user)
    similarUsers = []
    userDict = dict()

    for a in otherUserProfiles:
        if a.gender==gender or gender=="test":
            theirHobbies = a.hobby
            for aH in theirHobbies.all():
                for uH in userHobbies.all():
                    if aH==uH:
                        if ageFilter == "":
                            similarUsers.append(a)    
                        else:
                            if ageFilter=="lessThan10":
                                if a.age < 10:
                                    similarUsers.append(a)
                                    print("This user age in lessThan10")
                                    print(a.age)
                            elif ageFilter=="11-20":
                                if a.age > 10 and a.age < 21:
                                    similarUsers.append(a)
                                    print("This user age in 11-20")
                                    print(a.age)
                            elif ageFilter=="21-30":
                                if a.age > 20 and a.age < 31:
                                    similarUsers.append(a)
                                    print("This user age in 21-30")
                                    print(a.age)
                            elif ageFilter=="31-40":
                                if a.age > 30 and a.age < 41:
                                    similarUsers.append(a)
                                    print("This user age in 31-40")
                                    print(a.age)
                            elif ageFilter=="moreThan41":
                                if a.age > 40:
                                    similarUsers.append(a)
                                    print("this user age in moreThan41")
                                    print(a.age)

    allProfiles = serializers.serialize("json", similarUsers, indent = 2, use_natural_foreign_keys=True, 
    use_natural_primary_keys=True)
    print("Selected Gender is: ")
    print(gender)
    print(similarUsers)
    print(".")
    print(allProfiles)
    return JsonResponse(allProfiles, safe=False)

#method allowing users to create an account
def register(request):
    if request.method == 'POST':
        #uses a post method from html template
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #if valid it will save the form 
            user = form.save()
            #adds a new user in the model
            UserProfileModel.objects.create(user = user)
            login(request, user)
            #log user in !
            #redirects to the 2nd register page
            return redirect('/register2/')
    else: 
        form = UserCreationForm()
    return render (request, 'FriendZoneApp/register.html', {'form': form,'pageTitle': '- Register'})

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

def profile_view(request, userProfileID):
    userProfile = UserProfileModel.objects.get(id = userProfileID)
    
    context = {
        'userProfile' : userProfile
    }
    return render(request, 'FriendZoneApp/profile.html', context)

def addFriend(request, userProfileID, newFriendID):
    userProfile = UserProfileModel.objects.get(id = userProfileID)
    newFriendProfile = UserProfileModel.objects.get(id = newFriendID)
    friendName = userProfile.user
    userProfile.friend.add(newFriendProfile)
    send_mail('You have a new friend - FriendZone', str(friendName) + ' added you as a friend', 'friendzone720@gmail.com', recipient_list=[newFriendProfile.email])
    return index(request)

def addHobby(request, userProfileID, hobb):
    userProfile = UserProfileModel.objects.get(id = userProfileID)
    hobby = Hobby.objects.get(hobby=hobb)
    userProfile.hobby.add(hobby)
    userProfile.save()
    return index(request)

#method that allows users to edit thier profiles.
def editprofile_view(request):
    if request.method == 'POST':
        #uses ac custom django form from forms.py
        form = EditProfileForm(request.POST, instance = UserProfileModel.objects.get(user = request.user))
        if form.is_valid():
            #if valid it saves it and if it contains an image it will then save it in the model and direct to index
            updated_profile = form.save()
            if 'image' in request.FILES:
                updated_profile.image = request.FILES['image']
            updated_profile.save()
            return redirect('/index/')

    else:
        form = EditProfileForm(instance = UserProfileModel.objects.get(user = request.user))
        args = {'form': form}
        return render(request, 'FriendZoneApp/editprofile.html', args)

#this is the 2nd stage of user registration
def register2(request):
    if request.method == 'POST':
    #uses a custom django form which is called from forms.py
        form = RegisterForm(request.POST, instance = UserProfileModel.objects.get(user = request.user))
        if form.is_valid():
            #if form is valid then it will save in updated_profile, and if the form contains an image, then it will save to the model database
            updated_profile = form.save()
            if 'image' in request.FILES:
                updated_profile.image = request.FILES['image']
            updated_profile.save()
            #gets the current user details and then calculates the age from the DOB stored in the model
            member = UserProfileModel.objects.get(user = request.user)
            dob = member.dob
            dobYear = member.dob.year
            dobMonth = member.dob.month
            dobDay = member.dob.day
            #imports datetime to calculate current date
            today = date.today()
            ageAns = today.year - dobYear - ((today.month, today.day) < (dobMonth, dobDay))
            member.age = ageAns
            #once the age is calculated it then passes it back to the model and stores in under age
            member.save()
            print(dob)
            return redirect('/index/')

    else:
        form = RegisterForm(instance = UserProfileModel.objects.get(user = request.user))
        args = {'form': form}
        return render(request, 'FriendZoneApp/editprofile.html', args)

#method to allow user to change their passwords
def forgotpassword_view(request):
    if request.method == 'POST':
        #uses the django form Password change form
        form = PasswordChangeForm(data = request.POST, user = request.user)

        if form.is_valid():
            form.save()
            #if the form is valid it will save and redirect to login page, else direct to password page
            return redirect('/login/')
        else:
            return redirect('/password/')
    else:
        form = PasswordChangeForm(user = request.user)
        #sends the form to the html template
        args = {'form': form}
        return render(request, 'FriendZoneApp/password.html', args)

def listFriends(request, userProfileID):
    user = request.user
    userProfile = UserProfileModel.objects.get(user = user)
    userFriends = userProfile.friend
    context = {
        'loggedInUser' : user,
        'userProfile' : userProfile,
        'userFriends' : userFriends 
    }
    return render(request, 'FriendZoneApp/friends.html', context)

def removeFriend(request, userProfileID, friendID):
    user = request.user
    userProfile = UserProfileModel.objects.get(user = user)
    
    newFriendProfile = UserProfileModel.objects.get(id = friendID)
    friendName = userProfile.user
    userProfile.friend.remove(newFriendProfile)
    send_mail('You have lost a friend - FriendZone', str(friendName) + ' removed you as a friend, Inna lillahi wa inna ilayhi rajiun', 'friendzone720@gmail.com', recipient_list=[newFriendProfile.email])
    return listFriends(request, userProfile.id)


    





