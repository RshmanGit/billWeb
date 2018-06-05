from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.loginreq),
    url(r'^login/$', views.autho),
    url(r'login/', views.autho),
    url(r'^home/',views.home),
    url(r'^register/$',views.register),
    url(r'^register/registerReq/$',views.registerReq),
    url(r'^register/registerReq/login/',views.autho),
    url(r'^insertorders/$',views.insertOrder),
    url(r'^insertorders/insertReq/$',views.insertOrderReq),
    url(r'^insertrawMat/$',views.insertRawMat),
    url(r'^insertrawMat/insertReq/$',views.insertRawMatReq),
    url(r'^insertexps/$',views.insertExps),
    url(r'^insertexps/insertReq/$',views.insertExpsReq),
    url(r'^orders/', views.fullorders),
    url(r'^rawMat/', views.fullrawmat),
    url(r'^exps/', views.fullexps),
    url(r'^logout/$',views.logoutreq),
    url(r'editOrder/(?P<Id>[0-9]+)/$',views.updateOrder),
    url(r'editOrder/(?P<Id>[0-9]+)/updateReq/$',views.updateOrderReq),
    url(r'editRawMat/(?P<gatePass>[0-9]+)/$',views.updateRawMat),
    url(r'editRawMat/(?P<gatePass>[0-9]+)/updateReq/$',views.updateRawMatReq),
]
