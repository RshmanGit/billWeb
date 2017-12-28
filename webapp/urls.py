from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.loginreq),
    url(r'^login/', views.autho),
    url(r'^home/',views.home),
    url(r'^register/$',views.register),
    url(r'^register/registerReq/$',views.registerReq),
    url(r'^register/registerReq/login/',views.autho),
    url(r'^insertorders/$',views.insertOrder),
    url(r'^insertorders/insertReq/$',views.insertOrderReq),
]
