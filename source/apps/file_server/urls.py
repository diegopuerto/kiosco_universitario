from django.conf.urls import patterns, url
from . import views


urlpatterns = [
        url(r'^(?P<file_id>\d+)?/?$', views.insert_file, name='insert')
        ]
