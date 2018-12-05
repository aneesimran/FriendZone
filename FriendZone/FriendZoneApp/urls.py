from django.urls import path

from.import views
app_name='fz'

urlpatterns = [
    path('', views.login_view),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile')
]
