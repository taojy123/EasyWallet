
from django.conf.urls import url
from account import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^pay/$', views.pay, name='pay'),
]
