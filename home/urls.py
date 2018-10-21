from django.conf.urls import url, include
from . import views
app_name = 'home'

urlpatterns = [
    url(r'^$', views.Home, name='home'),
    url(r'^downloading//$', views.Downloading, name='downloading'), 
    url(r'^download-percentage/$', views.DownloadPercentage, name='download-percentage'), 
    url(r'^pause/$', views.Pause, name='pause'), 
    url(r'^play/$', views.Play, name='play'),
    url(r'^magnet-link/$', views.MagnetLink, name='magnet-link'), 

    
]
