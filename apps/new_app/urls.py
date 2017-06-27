from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^logout$', views.logout),
    url(r'^addbook$', views.addbook),
    url(r'^registerbook$', views.registerbook),
    url(r'^books/(?P<id>\d+)$', views.showbooks),
    url(r'^registerbook/(?P<id>\d+)$', views.registerbookshow),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^users/(?P<id>\d+)$', views.users),
]