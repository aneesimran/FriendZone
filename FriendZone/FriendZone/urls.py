from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('FriendZoneApp.urls')),
    path('FriendZoneApp/', include('password_reset.urls'))
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
