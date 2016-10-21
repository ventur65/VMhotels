from django.conf.urls import url, include
from . import views
urlpatterns = [
	#ex: /portal/change/
	url(r'^change/$', views.editpersdata, name='update_data'),
	#ex: /portal/personal/
	url(r'^personal/$', views.personal, name='personal'),
	#ex: /portal/logout/
	url(r'^logout/$', views.logout_view, name='logout_view'),
	#ex: /portal/register/costumer/
    url(r'^register/customer/$', views.RegistrationView.as_view(), name='registration_register_customer'),
    #ex: /portal/register/owner/
    url(r'^register/owner/$', views.RegistrationView.as_view(), name='registration_register_owner'),
    url(r'^', include('registration.backends.simple.urls')),
]
