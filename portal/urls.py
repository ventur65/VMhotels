from django.conf.urls import url
from . import views
urlpatterns = [
	#ex: /portal/
	url(r'^$', views.portal_welcome, name='portal_welcome'),
	url(r'^change/$', views.upload, name='update_data'),
	url(r'^personal/$', views.personal, name='personal'),
]
