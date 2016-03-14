from django.conf.urls import include, url
from application import views

urlpatterns = [
    url(r'^$', views.list, name='application_home_urls'),
    url(r'^(?P<id>\w+)/', include([
        url(r'^edit/$', views.edit, name='application_edit_urls'),
        url(r'^delete/$', views.delete, name='application_delete_urls'),
        url(r'^detail/$', views.detail, name='application_detail_urls'),
    ])),
]
