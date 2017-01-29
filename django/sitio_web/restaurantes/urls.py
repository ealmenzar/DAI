from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^hello/$', views.test, name='test'),
    url(r'^$', views.index, name='index'),
    url(r'^modifica/$', views.modify, name='modify'),
    url(r'^add/$', views.add, name='add'),
    url(r'^search/$', views.search, name='search'),
    url(r'^delete/$', views.delete, name='delete')
]