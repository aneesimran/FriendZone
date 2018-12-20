from django.urls import path
#from django.contrib.auth.views import (password_reset, password_reset_done, password_reset_confirm, password_reset_complete)
from.import views
app_name='fz'

urlpatterns = [
    path('', views.login_view),
    path('register/', views.register, name='register'),
    path('register2/', views.register2, name='register2'),
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:userProfileID>', views.profile_view, name='profile'),
    path('editprofile/', views.editprofile_view, name='editprofile'),
    path('password/', views.forgotpassword_view, name='forgotpassword'),
    path('addFriend/<int:userProfileID>/<int:newFriendID>/', views.addFriend, name='addFriend'),
    path('removeFriend/<int:userProfileID>/<int:friendID>/', views.removeFriend, name='removeFriend'),
    path('addHobby/<int:userProfileID>/<hobb>', views.addHobby, name='addHobby'),
    path('filterUsers/', views.filterUsers, name='filterUsers'),
    path('friends/<int:userProfileID>', views.listFriends, name='listFriends')
]
