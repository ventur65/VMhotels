from django.conf.urls import url, include
from . import views
urlpatterns = [
	#ex: /portal/
	url(r'^$', views.portal_welcome, name='portal_welcome'),
	url(r'^change/$', views.upload, name='update_data'),
	url(r'^personal/$', views.personal, name='personal'),
	url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^register/$', views.RegistrationView.as_view(), name='registration_register'),
    url(r'^', include('registration.backends.simple.urls')),
]
