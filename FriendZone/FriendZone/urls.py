from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('FriendZoneApp.urls'))
] + static(settings.MEDIA.URL, document_root = settings.MEDIA_ROOT)
