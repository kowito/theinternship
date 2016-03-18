from django.conf.urls import include, url
from application import views

urlpatterns = [
    url(r'^$', views.list, name='application_home_urls'),
    url(r'^review/$', views.application_review, name='application_review_urls'),
    url(r'^result/$', views.application_result, name='application_result_urls'),
    url(r'^process/$', views.process_new_application,
        name='application_process_urls'),
    url(r'^(?P<id>\w+)/', include([
        url(r'^edit/$', views.edit, name='application_edit_urls'),
        url(r'^delete/$', views.delete, name='application_delete_urls'),
        url(r'^detail/$', views.detail, name='application_detail_urls'),
        url(r'^my_vote/(?P<score>\w+)$', views.my_vote, name='my_vote_urls'),
        url(r'^vote/(?P<score>\w+)$', views.vote, name='application_vote_urls'),
    ])),
]
