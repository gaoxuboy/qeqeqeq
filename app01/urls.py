


from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
urlpatterns = [

    url(r'^(?P<article_type_id>\d+)/', views.index),
    url(r'^(?P<user_site>\w+)/active/(?P<condition>category|tag|data)/(?P<para>\w+）)', views.homgsite),
    url(r'^(?P<user_site>\w+)/active/(?P<active_id>\d+)', views.useregon),


    url(r'^(?P<user_site>\w+)/', views.homgsite),





]
