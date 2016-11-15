from datetime import datetime, timedelta
from django.contrib.auth.models import User
from hotels.models import Room, Hotel
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from .models import Reservation
from .views import *
from .forms import ReservationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class AddReservationViewTests(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		
	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create_user(username='prova', email='ciao@mail.it', password='prova')
		new_group, created = Group.objects.get_or_create(name='customers')
		cls.owner = User.objects.create_user(username='owner', email='owner@mail.it', password='owner')
		ct = ContentType.objects.get_for_model(Reservation)
		permission = Permission.objects.get(codename="add_reservation")
		new_group.permissions.add(permission)
		cls.user.groups.add(new_group)
		cls.user.user_permissions = [permission]
		cls.hotel = Hotel.objects.create(name = 'ciao', user = cls.owner)
		cls.room = Room.objects.create(hotel=cls.hotel, number = 1, cost = 1)
		iidate = datetime.now().date()
		ffdate = datetime.now().date() + timedelta(days=7)
		cls.res = Reservation.objects.create(user = cls.user, idate = iidate, fdate = ffdate, room = cls.room, firstname = 'giovanni', is_active = True)
		
	def test_add_reservation_with_invalid_date(self):
		self.client.login(username='prova', password='prova')
		data = {
    		'firstname': 'john',
    		'lastname': 'prov',
    		'idate': 'ciao',
    		'fdate': "2016-11-23",
    		'city': 'fabbrico',
    		'address': 'ciao',
    		'email': 'prova@gmail.com',
    		'tel_0': "+39",
    		'tel_1': '3335661379',
    		'Ok': "Ok",
    	}
   		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), data = data)
   		request.user = self.user
   		response = add_reservation(request, self.hotel.pk, self.room.pk)
   		print response
   		self.assertContains(response, 'Enter a valid date.')
    	
	def test_add_reservation(self):
		self.client.login(username='prova', password='prova')
		response = self.client.get(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)))
		self.assertEqual(response.status_code, 200)
