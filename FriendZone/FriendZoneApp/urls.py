from django.urls import path

from.import views

urlpatterns = [
    path('', views.register, name = "register"),
    path('register/', views.regisster),
    path('index/', views.index)
    
]
