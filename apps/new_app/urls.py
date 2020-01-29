from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^logout$', views.logout),
    url(r'^travels/add$', views.addtravel),
    url(r'^createtravel$', views.createtravel),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^travels/destination/(?P<id>\d+)$', views.destination),
]
