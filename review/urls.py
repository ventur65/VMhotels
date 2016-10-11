from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^(?P<hotel_id>[0-9]+)/add/$', views.add_review, name='add_review'),
	url(r'^(?P<hotel_id>[0-9]+)/$', views.ReviewListView.as_view(), name='list_review'),
]
