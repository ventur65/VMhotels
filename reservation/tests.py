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
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth.models import AnonymousUser
from django.test import Client
from django.http import Http404
from django.contrib.messages import get_messages

class AddReservationViewTests(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		
	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create_user(username='prova', email='ciao@mail.it', password='prova')
		customers, created = Group.objects.get_or_create(name='customers')
		owners, c = Group.objects.get_or_create(name='owners')
		cls.owner = User.objects.create_user(username='owner', email='owner@mail.it', password='owner')
		ct = ContentType.objects.get_for_model(Reservation)
		permission = Permission.objects.get(codename="add_reservation")
		customers.permissions.add(permission)
		cls.user.groups.add(customers)
		cls.user.user_permissions = [permission]
		cls.hotel = Hotel.objects.create(name = 'ciao', user = cls.owner)
		cls.room = Room.objects.create(hotel=cls.hotel, number = 1, cost = 1)
		iidate = datetime.now().date()
		ffdate = datetime.now().date() + timedelta(days=7)
		cls.res = Reservation.objects.create(user = cls.user, idate = iidate, fdate = ffdate, room = cls.room, firstname = 'giovanni', is_active = True)
		cls.hotel2 = Hotel.objects.create(name = 'hotel2', user = cls.owner, email='gg@gg.it', tel='0522650200', city='roma')
		cls.room2 = Room.objects.create(hotel=cls.hotel2, number = 2, cost = 1)
	
	def test_add_reservation_denies_anonymous(self):
		#GET
		request = self.factory.get(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), follow = True)
		request.user = AnonymousUser()
		self.assertTrue(request.user.is_anonymous)
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		response.client = Client()
#		response.client.login(username = 'prova', password = 'prova')
		self.assertEqual(response.get('location'), reverse('portal:django.contrib.auth.views.login')+
							'?next='+reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)))
		#POST
		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), follow = True)
		request.user = AnonymousUser()
		self.assertTrue(request.user.is_anonymous)
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		self.assertEqual(response.get('location'), reverse('portal:django.contrib.auth.views.login')+
							'?next='+reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)))
		
	def test_add_reservation_user_without_perm(self):
		user_no_perm = User.objects.create_user(username='noperm', email='permission@mail.it', password='nopermission')
		#GET
		request = self.factory.get(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), follow = True)
		request.user = user_no_perm
		self.assertTrue(request.user.is_authenticated)
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		response.client = Client()
		response.client.login(username = 'noperm', password = 'nopermission')
		self.assertEqual(response.get('location'), reverse('portal:django.contrib.auth.views.login')+
							'?next='+reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)))
		#POST
		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), follow = True)
		request.user = user_no_perm
		self.assertTrue(request.user.is_authenticated)
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		response.client = Client()
		response.client.login(username = 'noperm', password = 'nopermission')
		self.assertEqual(response.get('location'), reverse('portal:django.contrib.auth.views.login')+
							'?next='+reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)))
	
	def test_add_reservation_get_user_with_perm(self):
		request = self.factory.get(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), follow = True)
		request.user = self.user
		self.assertTrue(request.user.is_authenticated)
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		self.assertEqual(response.status_code, 200)
		
	def test_add_reservation_adding_successful(self):
		valid_idate = datetime.now().date() + timedelta(days=8)
		valid_fdate = datetime.now().date() + timedelta(days=10)
		data = {
    			'firstname': 'john',
    			'lastname': 'prov',
    			'idate': valid_idate,
    			'fdate': valid_fdate,
    			'city': 'fabbrico',
    			'address': 'ciao',
    			'email': 'prova@gmail.com',
    			'tel_0': "+39",
    			'tel_1': '3335661379',
    			'Ok': "Ok",
    		}
		res_form = ReservationForm(data=data)
		self.assertTrue(res_form.is_valid())
   		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), data = data, follow = True)
   		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)
   		request.user = self.user
   		response = add_reservation(request, self.hotel.pk, self.room.pk)		
   		r = Reservation.objects.get(firstname='john')
   		response.client = Client()
   		response.client.login(username='prova', password='prova')
   		self.assertEqual(response.get('location'), reverse('portal:personal'))
   		self.assertIsNotNone(r)
   		self.assertEqual(r.firstname, 'john')
   		self.assertEqual(r.lastname, 'prov')
   		self.assertEqual(r.idate, valid_idate)
   		self.assertEqual(r.fdate, valid_fdate)
   		self.assertEqual(r.city, 'fabbrico')
   		self.assertEqual(r.address, 'ciao')
   		self.assertEqual(r.email, 'prova@gmail.com')
   		self.assertEqual(r.tel, '+393335661379')
   		self.assertTrue(r.is_active)
   	
   	def test_add_reservation_in_queue(self):
   		idate_already_exists = datetime.now().date()
   		fdate_already_exists = datetime.now().date() + timedelta(days = 4)
   		data = {
   			'firstname': 'john',
   			'lastname': 'prov',
   			'idate': idate_already_exists,
   			'fdate': fdate_already_exists,
   			'city': 'fabbrico',
   			'address': 'via don sturzo',
   			'email': 'prova@gmail.com',
   			'tel_0': '+39',
   			'tel_1': '3335661379',
   			'Ok': 'Ok',
   		}
   		request = self.factory.post(reverse('reservation:add_reservation', args=(self.hotel.pk, self.room.pk)), data = data, follow = True)
   		setattr(request, 'session', 'session')
   		messages = FallbackStorage(request)
   		setattr(request, '_messages', messages)
   		request.user = self.user
   		response = add_reservation(request, self.hotel.pk, self.room.pk)
   		response.client = Client()
   		response.client.login(username='prova', password='prova')
   		self.assertEqual(response.get('location'), reverse('portal:personal'))
   		r = Reservation.objects.get(firstname='john')
   		self.assertFalse(r.is_active)
   		
	def test_add_reservation_with_blank_data(self):
		data = {
			'Ok': 'Ok'
		}
		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), data = data)
		request.user = self.user
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		self.assertEqual(response.status_code, 200)
		
		
	def test_add_reservation_with_invalid_date(self):
		invalid_idate = 'invalid'
		valid_fdate = datetime.now().date() + timedelta(days=7)
    		data = {
			'firstname': 'john',
			'lastname': 'prov',
			'idate': invalid_idate,
			'fdate': valid_fdate,
			'city': 'fabbrico',
			'address': 'ciao',
			'email': 'prova@gmail.com',
			'tel_0': "+39",
			'tel_1': '3335661379',
			'Ok': "Ok",
		}
		form = ReservationForm(data)
		self.assertFalse(form.is_valid())
		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), data = data)
		request.user = self.user
		response = add_reservation(request, self.hotel.pk, self.room.pk)
#		print response
		self.assertContains(response, 'Enter a valid date.')
		
	def test_add_reservation_with_date_in_the_past(self):
		past_idate = datetime.now().date() + timedelta(days = -7)
		past_fdate = datetime.now().date() + timedelta(days = -4)
		data = {
			'firstname': 'john',
			'lastname': 'prov',
			'idate': past_idate,
			'fdate': past_fdate,
			'city': 'fabbrico',
			'address': 'ciao',
			'email': 'prova@gmail.com',
			'tel_0': "+39",
			'tel_1': '3335661379',
			'Ok': "Ok",
		}
		form = ReservationForm(data)
		self.assertFalse(form.is_valid())
		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), data = data)
		request.user = self.user
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		self.assertContains(response, 'Date in the past')
	
	def test_add_reservation_with_invalid_hotel(self):
		invalid_hotel_id = 55
		data = dict()
#		GET
		request = self.factory.get(reverse('reservation:add_reservation', args = (invalid_hotel_id, self.room.pk)), follow = True)
   		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)
   		request.user = self.user	
   		with self.assertRaises(Http404):
   			response = add_reservation(request, invalid_hotel_id, self.room.pk)
#		POST		
   		request = self.factory.post(reverse('reservation:add_reservation', args = (invalid_hotel_id, self.room.pk)), data=data,  follow = True)
   		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)
   		request.user = self.user	
   		with self.assertRaises(Http404):
   			response = add_reservation(request, invalid_hotel_id, self.room.pk)
   	
   	def test_add_reservation_with_invalid_room(self):
   		#GET
   		request = self.factory.get(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room2.pk)), follow = True)
   		setattr(request, 'session', 'session')
   		messages = FallbackStorage(request)
   		setattr(request, '_messages', messages)
   		request.user = self.user
   		response = add_reservation(request, self.hotel.pk, self.room2.pk)
   		response.client = Client()
   		response.client.login(username='prova', password = 'prova')
   		self.assertTrue(self.hotel.pk != self.room2.hotel.pk)
   		self.assertEqual(response.get('location'), reverse('portal:personal'))
   		#POST
   		data = dict()
   		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room2.pk)), data = data, follow = True)
   		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)
   		request.user = self.user
   		response = add_reservation(request, self.hotel.pk, self.room2.pk)
   		storage = get_messages(request)
   		message = None
   		for mm in storage:
   			message = mm
   		response.client = Client()
   		response.client.login(username='prova', password='prova')
   		self.assertTrue(self.hotel.pk != self.room2.hotel.pk)
   		self.assertEqual(response.get('location'), reverse('portal:personal'))
   		self.assertEqual(str(message),'This room is not in this Hotel.')
