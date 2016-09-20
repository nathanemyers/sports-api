from django.conf.urls import url

from . import views

app_name = 'nbapowerranks'
urlpatterns = [
        url(r'rankings/(?P<year>[0-9]+)/(?P<week>[0-9]+)', views.week_rankings),
        url(r'rankings/(?P<year>[0-9]+)', views.year_rankings),
        url(r'rankings/info', views.info),
        ]
