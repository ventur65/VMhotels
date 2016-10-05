from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^addreservation/$', views.add_reservation, name="add_reservation"),
]
