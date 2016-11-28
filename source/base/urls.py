from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from apps.DaneUsers.views.LoginView import LoginView
from filebrowser.sites import site
admin.autodiscover()
admin.site.login = login_required(admin.site.login)


urlpatterns = [
    url(r'^control/login', LoginView.as_view()),
    url(r'^control/', include(admin.site.urls)),
    url(r'^kiosco/', include('apps.kiosco_app.urls',  namespace = "kiosco_app")),
    url(r'^users/', include('apps.DaneUsers.urls',  namespace = "DaneUsers")),
    url(r'^statistical_society/', include('apps.statistical_society.urls',  namespace = "statistical_society")),
    url(r'^services_requests/', include('apps.services_requests.urls',  namespace = "services_requests")),
    url(r'^chaining/', include('libs.django_smart_selects.smart_selects.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^storage/', include('apps.storage_files_server.urls')),
#     url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^shop/', include('apps.shop.urls', namespace = "shop")),
#    url(r'^cart/', include('apps.cart.urls', namespace = "cart")),
    url(r'^file_server/', include('apps.file_server.urls', namespace = "file_server")),
    url(r'^$', include('apps.kiosco_app.urls'))]
