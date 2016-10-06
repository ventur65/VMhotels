from django.conf.urls import url, include
from . import views

urlpatterns = [
	#ex: /hotels/1/
	url(r'^(?P<pk>[0-9]+)/$', views.HotelDetailView.as_view(),
	name='hotel_detail'),
	#ex: /hotels/1/2/
	url(r'^(?P<hotel_id>[0-9]+)/(?P<room_id>[0-9]+)/$', views.room_detail,
	name = 'room_detail'),
	#ex: /hotels/createhotel/
	url(r'^createhotel/$', views.create_hotel, name = 'create_hotel'),
	#ex: /hotels/5/createroom/
	url(r'^(?P<hotel_id>[0-9]+)/createroom/$', views.create_room, name = 'create_room'),
	#ex: /hotels/5/edithotel/
	url(r'^(?P<hotel_id>[0-9]+)/edithotel/$', views.edit_hotel, name='edit_hotel'),
	#ex: /hotels/1/2/editroom
	url(r'^(?P<hotel_id>[0-9]+)/(?P<room_id>[0-9]+)/editroom/$', views.edit_room, name='edit_room'),
]
