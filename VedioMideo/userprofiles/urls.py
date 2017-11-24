from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout$', auth_views.logout, {'next_page': '/'}, name='logout',),
    url(r'^subir$', views.subir, name='subir'),
    url(r'^video/(?P<pk>[0-9]+)/$', views.video_details, name='video_details'),
]