from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^(?P<hotel_id>[0-9]+)/(?P<room_id>[0-9]+)/add/$', views.add_reservation, name="add_reservation"),
	url(r'^(?P<reservation_id>[0-9]+)/$', views.reservation_detail, name="reservation_detail"),
	url(r'^(?P<reservation_id>[0-9]+)/editres$', views.edit_reservation, name="edit_reservation"),
	url(r'^(?P<reservation_id>[0-9]+)/delres$', views.delete_reservation, name="delete_reservation"),
]
