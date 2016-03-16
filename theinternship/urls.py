from django.conf.urls import url, include
from django.contrib import admin
from theinternship.views import home, profile

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^accounts/profile/$', profile),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^application/', include('application.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
