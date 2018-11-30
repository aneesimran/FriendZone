from django.urls import path

from.import views
app_name='fz'

urlpatterns = [
    path('', views.register),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    #path('login/', views.login_view, name='login'),
    
]
