from django.conf.urls import url
from . import views

urlpatterns = [
	#ex: /hotels/1/
	url(r'^(?P<hotel_id>[0-9]+)/$', views.hotel_detail,
	name='hotel_detail'),
	#ex: /hotels/1/2/
	url(r'^(?P<hotel_id[0-9]+)/(?P<room_id[0-9]+)/$', views.room_detail,
	name = 'room_detail'),
]
