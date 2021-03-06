from django.conf.urls import url

from .admin_site import bcpp_clinic_screening_admin
from .views import ListBoardView
from django.contrib import admin

app_name = 'bcpp_clinic_screening'
screening_identifier = '[0-9A-Z]{7}'

admin.autodiscover()


def listboard_urls():
    urlpatterns = []

    listboard_configs = [
        ('listboard_url', ListBoardView, 'listboard')]
    for listboard_url_name, listboard_view_class, label in listboard_configs:
        urlpatterns.extend([
            url(r'^' + label + '/'
                '(?P<screening_identifier>' + screening_identifier + ')/'
                '(?P<page>\d+)/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/'
                '(?P<screening_identifier>' + screening_identifier + ')/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/(?P<page>\d+)/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/',
                listboard_view_class.as_view(), name=listboard_url_name)])
    return urlpatterns


urlpatterns = [
    url(r'^admin/', bcpp_clinic_screening_admin.urls)] + listboard_urls()
