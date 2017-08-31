from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.UserIndexView.as_view(), name='index'),
	url(r'^add/$', views.UserAddView.as_view(), name='add'),
	url(r'^view/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='view'),
	url(r'^edit/(?P<pk>[0-9]+)/$', views.UserEditView.as_view(), name='edit'),
	url(r'^delete/(?P<pk>[0-9]+)/$', views.UserDeleteView.as_view(), name='delete'),
	url(r'^(?P<result>.*)$', views.UserIndexView.as_view(), name='index'),
]
