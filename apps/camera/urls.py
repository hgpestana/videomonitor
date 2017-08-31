from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CameraIndexView.as_view(), name='index'),
    url(r'^add/$', views.CameraAddView.as_view(), name='add'),
    url(r'^view/(?P<pk>[0-9]+)/$', views.CameraDetailView.as_view(), name='view'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.CameraEditView.as_view(), name='edit'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.CameraDeleteView.as_view(), name='delete'),
    url(r'^(?P<result>.*)$', views.CameraIndexView.as_view(), name='index'),
]
