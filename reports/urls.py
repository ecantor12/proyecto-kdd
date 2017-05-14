from django.conf.urls import include, url
from . import views

urlpatterns = [
        url(r'^$', views.reports),
        url(r'^attention_period/$', views.attention_period),
    ]