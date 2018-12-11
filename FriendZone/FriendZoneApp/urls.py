from django.urls import path

from.import views
app_name='fz'

urlpatterns = [
    path('', views.login_view),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:userProfileID>', views.profile_view, name='profile'),
    path('editprofile/', views.editprofile_view, name='editprofile'),
    path('password/', views.forgotpassword_view, name='forgotpassword'),
    path('addFriend/<int:userProfileID>/<int:newFriendID>/', views.addFriend, name='addFriend'),
    path('addHobby/<int:userProfileID>/<hobb>', views.addHobby, name='addHobby')
]
