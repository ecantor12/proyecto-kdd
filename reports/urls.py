from django.conf.urls import include, url
from . import views

urlpatterns = [
        url(r'^$', views.reports),
        url(r'^attention_period/$', views.attention_period),
        url(r'^attention_day/$', views.attention_day),
        url(r'^medicine_prescription/$', views.medicine_prescription),
        url(r'^products_together/$', views.products_together),
    ]