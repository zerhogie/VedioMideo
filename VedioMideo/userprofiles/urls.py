from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.VideoListView.as_view(), name='index'),
    url(r'^logout$', auth_views.logout, {'next_page': '/'}, name='logout',),
    url(r'^addusers$', views.addusers, name='addusers'),
    url(r'^subir$', views.subir, name='subir'),
    url(r'^video/(?P<pk>[0-9]+)/$', views.VideoDetailView.as_view(), name='video_details'),
    url(r'^mostrando/(?P<orden>\w+)/$', views.mostrar, name='mostrar')
]
