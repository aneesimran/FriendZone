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
from django.contrib.auth.decorators import login_required

# login decorator needed for specific views to be accessible

#index used to display similar users with similar hobbies as logged in user
@login_required
def index(request):
    user = request.user
    userProfile = UserProfileModel.objects.get(user = user)
    userHobbies = userProfile.hobby
    otherUserProfiles = UserProfileModel.objects.exclude(user = request.user) #excluding logged in user
    similarUsers = []
    
    #for loops to add users who have at least 1 same hobby as the logged in user and add them to the list
    for a in otherUserProfiles:
        theirHobbies = a.hobby
        for aH in theirHobbies.all():
            for uH in userHobbies.all():
                if aH==uH:
                    similarUsers.append(a)    

    sortedUsers = []
    copySimUsers = similarUsers[:]

    #creating temporary dictionaries to display the data in html template
    for sUser in copySimUsers: 
        temp = {
            0: sUser.id,
            1: sUser.first_name, 
            2: sUser.last_name, 
            3: sUser.hobby.all(),
            'count': sUser.hobby.all().count()
        }
        sortedUsers.append(temp) #adding dictinary to the list

    sortedUsers.sort(key=operator.itemgetter('count'), reverse = True) #sorting the users in the list by count of hobbies
    #and sorting them in descending order
    
    #context to display the data in the html template
    context = {
        'loggedInUser' : user,
        'userProfile' : userProfile,
        'similarUsers' : similarUsers,
        'oUP' : otherUserProfiles,
        'sortedUsers': sortedUsers
    }
    return render(request, 'FriendZoneApp/index.html', context) # rendering required page with the context needed


#method to find users by age and/or gender
def filterUsers(request):
    gender = request.GET['gender'] #chosen gender from Ajax request
    ageFilter = request.GET['chosenAge'] #chosen age from Ajax request

    user = request.user
    userProfile = UserProfileModel.objects.get(user = user)
    userHobbies = userProfile.hobby
    otherUserProfiles = UserProfileModel.objects.exclude(user = request.user)
    similarUsers = []

    #adds each user if they meet certain condtitions such as age range
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
    use_natural_primary_keys=True) #serialising into JSON form
    return JsonResponse(allProfiles, safe=False) # returnign JSON response

#method to create a new user 
def register(request):
    if request.method == 'POST':
        #uses a post method from html template
        form = UserCreationForm(request.POST)
        #if valid it will save the form 
        if form.is_valid():
            user = form.save()
            #adds a new user in the model
            UserProfileModel.objects.create(user = user)
            #log user in 
            login(request, user)
            #redirects to the 2nd register page
            return redirect('/register2/')
    else: 
        form = UserCreationForm()
    return render (request, 'FriendZoneApp/register.html', {'form': form,'pageTitle': '- Register'})

#method to validate user login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): 
            #log the user in 
            user = form.get_user()
            login(request, user) #built in log in
            return redirect('/index/')
    else: 
        form = AuthenticationForm() #if not POST, then it will be empty
    return render (request, 'FriendZoneApp/login.html', {'form': form, 'pageTitle': '- Login'})

#method to log user out
def logout_view(request):
    if request.method == 'POST':
        logout(request) #built in log out
        return redirect('/login/')

#method to view a users profile
@login_required
def profile_view(request, userProfileID):
    userProfile = UserProfileModel.objects.get(id = userProfileID) #acquring user profile of a user to view their profile
    context = {
        'userProfile' : userProfile
    }
    return render(request, 'FriendZoneApp/profile.html', context) #rendering the generic profile page, displaying contents of the context

# method to add a friend (user profile) to another user
@login_required
def addFriend(request, userProfileID, newFriendID):
    userProfile = UserProfileModel.objects.get(id = userProfileID) # acquring logged in users profile object
    newFriendProfile = UserProfileModel.objects.get(id = newFriendID) # acquiring profile object of person to add as friend
    friendName = userProfile.user # used to display user in email when sent
    userProfile.friend.add(newFriendProfile) # adding the new user to logged in users friends list to database 

    #sending the email
    send_mail('You have a new friend - FriendZone', str(friendName) + ' added you as a friend', 'friendzone720@gmail.com', recipient_list=[newFriendProfile.email])
    return index(request) # going back to index.html 

#method to add a hobby to logged in user's user profile 
@login_required
def addHobby(request, userProfileID, hobb):
    userProfile = UserProfileModel.objects.get(id = userProfileID) # acquring logged in user's user profiile
    hobby = Hobby.objects.get(hobby=hobb) # acquring the hobby object needed from database
    userProfile.hobby.add(hobby) # adding the hobby object to users user profile 
    userProfile.save() # saving changes to database
    return index(request)

#method that allows users to edit thier profiles.
@login_required
def editprofile_view(request):
    if request.method == 'POST':
        #uses ac custom django form from forms.py
        form = EditProfileForm(request.POST, instance = UserProfileModel.objects.get(user = request.user))
        if form.is_valid():  #if valid it saves it and if it contains an image it will then save it in the model and direct to index
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
        if form.is_valid():  #if form is valid then it will save in updated_profile, and if the form contains an image, then it will save to the model database
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
            #once the age is calculated it then passes it back to the model and stores in under age
            member.age = ageAns
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

        #if the form is valid it will save and redirect to login page, else direct to password page
        if form.is_valid():
            form.save()
            
            return redirect('/login/')
        else:
            return redirect('/password/')
    else:
        form = PasswordChangeForm(user = request.user)
        #sends the form to the html template
        args = {'form': form}
        return render(request, 'FriendZoneApp/password.html', args)

#method to display users current friends
@login_required
def listFriends(request, userProfileID):
    user = request.user
    userProfile = UserProfileModel.objects.get(user = user) # acquring logged in user's user profile
    userFriends = userProfile.friend # acquring logged in users friends
    context = {
        'loggedInUser' : user,
        'userProfile' : userProfile,
        'userFriends' : userFriends 
    } # contect to display user and theri friends
    return render(request, 'FriendZoneApp/friends.html', context)

# method to remove a friends from users list of friends
@login_required
def removeFriend(request, userProfileID, friendID):
    user = request.user
    userProfile = UserProfileModel.objects.get(user = user) #acquring logged in user's user profile to make changes to
    
    friendProfile = UserProfileModel.objects.get(id = friendID) # acquring the user profile of the person to remove 
    friendName = userProfile.user #used to display name in email
    userProfile.friend.remove(friendProfile) # removing the friend from the users list of friends

    #sending email to notify that this person has removed you from their list of friends
    send_mail('You have lost a friend - FriendZone', str(friendName) + ' removed you as a friend, Inna lillahi wa inna ilayhi rajiun', 'friendzone720@gmail.com', recipient_list=[friendProfile.email])
    return listFriends(request, userProfile.id)