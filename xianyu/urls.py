"""
@UpdateTime: 2017/12/7
@Author: liutao
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^moblephone/$', views.moblephone, name='moblephone'),
    url(r'^detail/$', views.detail, name='detail'),
    url(r'^ap/$', views.addproduct, name='addproduct'),
    url(r'^exit/$', views.exit, name='exit'),
]
