from django.conf.urls import patterns, url
from . import views


urlpatterns = [
    url(r'^(?P<file_id>\d+)?/?$', views.insert_file, name='insert'),
    url(r'^pending/$', views.pending_files, name='pending'),
    url(r'^public/$', views.public_file_list, name='public'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^all/$', views.all_files_list, name='all'),
    url(r'^$', views.insert_file, name='insert'),
]
