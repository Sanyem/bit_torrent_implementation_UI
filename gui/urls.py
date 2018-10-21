from django.conf.urls import url, include
from . import views
app_name = 'gui'

urlpatterns = [
    url(r'^$', views.selectFile, name='selectFile'),
    url(r'^percentage/$', views.percentage, name='percentage'),
]
