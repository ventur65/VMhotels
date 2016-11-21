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

class Check_Update_Tests(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		
	@classmethod
	def setUpTestData(cls):
		cls.owner = User.objects.create_user(username = 'owner', email = 'owner@mail.it', password='owner')
		cls.customer = User.objects.create_user(username='customer', email = 'customer@mail.it', password='customer')
		cls.h1 = Hotel.objects.create(name = 'h1', user = cls.owner)
		cls.room = Room.objects.create(hotel = cls.h1, number = 1, cost = 1)
		idate = datetime.now().date() + timedelta(days = 10)
		fdate = datetime.now().date() + timedelta(days = 20)
		cls.res1 = Reservation.objects.create(user = cls.customer, idate = idate, 
						fdate = fdate, room = cls.room, is_active = True, firstname='res1')
	
	def test_check_res(self):
		idate_in_period = datetime.now().date() + timedelta(days = 15)
		idate_out_period = datetime.now().date() + timedelta(days = 5)
		fdate_in_period = datetime.now().date() + timedelta(days = 17)
		fdate_out_period = datetime.now().date() + timedelta(days = 25)
		
		res2 = Reservation.objects.create(user = self.customer, idate = idate_in_period,
					fdate = fdate_out_period, room = self.room, firstname = 'res2', is_active = False)
		res3 = Reservation.objects.create(user = self.customer, idate = idate_out_period,
					fdate = fdate_in_period, room = self.room, firstname = 'res3', is_active = False)
		res4 = Reservation.objects.create(user = self.customer, idate = idate_in_period,
					fdate = fdate_in_period, room = self.room, firstname = 'res4', is_active = False)
		res5 = Reservation.objects.create(user = self.customer, idate = idate_out_period,
					fdate = fdate_out_period, room = self.room, firstname = 'res5', is_active = False)
		idate_ok = idate_out_period
		fdate_ok = datetime.now().date()+timedelta(days=8)
		res6 = Reservation.objects.create(user = self.customer, idate = idate_ok,
					fdate = fdate_ok, room = self.room, firstname = 'res6', is_active = False)
					
		self.assertFalse(check_res(res2, self.room))
		self.assertFalse(check_res(res3, self.room))
		self.assertFalse(check_res(res4, self.room))
		self.assertFalse(check_res(res5, self.room))
		self.assertTrue(check_res(res6, self.room))
		
	def test_update_state_res(self):
		idate_res2 = datetime.now().date() + timedelta(days = 30)
		fdate_res2 = datetime.now().date() + timedelta(days = 40)
		res2 = Reservation.objects.create(user = self.customer, idate = idate_res2,
					fdate = fdate_res2, room = self.room, firstname = 'res2', is_active = False)
		res3 = Reservation.objects.create(user = self.customer, idate = idate_res2,
					fdate = fdate_res2, room = self.room, firstname = 'res3', is_active = False)
		self.assertFalse(res2.is_active)
		self.assertFalse(res3.is_active)
		self.assertTrue(check_res(res2, self.room))
		self.assertTrue(check_res(res3, self.room))
		update_state_res(self.room)
		res2 = Reservation.objects.get(firstname = 'res2')
		res3 = Reservation.objects.get(firstname = 'res3')
		self.assertTrue(self.res1.is_active)
		self.assertTrue(res2.is_active)
		self.assertFalse(res3.is_active)
		self.assertFalse(check_res(res3, self.room))

class AddReservationViewTests(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		
	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create_user(username='prova', email='prova@mail.it', password='prova')
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
	
	def create_res_data(self, idate, fdate):
		data = {
    			'firstname': 'john',
    			'lastname': 'prov',
    			'idate': idate,
    			'fdate': fdate,
    			'city': 'fabbrico',
    			'address': 'ciao',
    			'email': 'prova@gmail.com',
    			'tel_0': "+39",
    			'tel_1': '3335661379',
    			'Ok': "Ok",
		}
		return data
			
	def test_add_reservation_denies_anonymous(self):
		#GET
		request = self.factory.get(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), follow = True)
		request.user = AnonymousUser()
		self.assertTrue(request.user.is_anonymous())
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		self.assertEqual(response.get('location'), reverse('portal:django.contrib.auth.views.login')+
							'?next='+reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)))
		#POST
		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), follow = True)
		request.user = AnonymousUser()
		self.assertTrue(request.user.is_anonymous())
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		self.assertEqual(response.get('location'), reverse('portal:django.contrib.auth.views.login')+
							'?next='+reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)))
		
	def test_add_reservation_user_without_perm(self):
		user_no_perm = User.objects.create_user(username='noperm', email='permission@mail.it', password='nopermission')
		#GET
		request = self.factory.get(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), follow = True)
		request.user = user_no_perm
		self.assertTrue(request.user.is_authenticated())
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		self.assertEqual(response.get('location'), reverse('portal:django.contrib.auth.views.login')+
							'?next='+reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)))
		#POST
		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), follow = True)
		request.user = user_no_perm
		self.assertTrue(request.user.is_authenticated())
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		self.assertEqual(response.get('location'), reverse('portal:django.contrib.auth.views.login')+
							'?next='+reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)))
	
	def test_add_reservation_get_user_with_perm(self):
		request = self.factory.get(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), follow = True)
		request.user = self.user
		self.assertTrue(request.user.is_authenticated())
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		self.assertEqual(response.status_code, 200)
		
	def test_add_reservation_adding_successful(self):
		valid_idate = datetime.now().date() + timedelta(days=8)
		valid_fdate = datetime.now().date() + timedelta(days=10)
		data = self.create_res_data(valid_idate, valid_fdate)
		res_form = ReservationForm(data=data)
		self.assertTrue(res_form.is_valid())
   		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), data = data, follow = True)
   		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)
   		request.user = self.user
   		response = add_reservation(request, self.hotel.pk, self.room.pk)
   		storage = get_messages(request)
   		message = []
   		for mm in storage:
   			message.append(mm)	
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
   		self.assertEqual(len(message), 1)
   		self.assertEqual(str(message[0]),'The reservation is successfully added.')
   	
   	def test_add_reservation_in_queue(self):
   		idate_already_exists = datetime.now().date()
   		fdate_already_exists = datetime.now().date() + timedelta(days = 4)
   		data = self.create_res_data(idate_already_exists, fdate_already_exists)
   		request = self.factory.post(reverse('reservation:add_reservation', args=(self.hotel.pk, self.room.pk)), data = data, follow = True)
   		setattr(request, 'session', 'session')
   		messages = FallbackStorage(request)
   		setattr(request, '_messages', messages)
   		request.user = self.user
   		response = add_reservation(request, self.hotel.pk, self.room.pk)
   		storage = get_messages(request)
   		message = []
   		for mm in storage:
   			message.append(mm)	
   		response.client = Client()
   		response.client.login(username='prova', password='prova')
   		self.assertEqual(response.get('location'), reverse('portal:personal'))
   		r = Reservation.objects.get(firstname='john')
   		self.assertFalse(r.is_active)
   		self.assertEqual(len(message), 1)
   		self.assertEqual(str(message[0]),'Your reservation has been added to a queue: if the previous reservations are deleted, you will receive an email.')
   		
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
		data = self.create_res_data(invalid_idate, valid_fdate)
		form = ReservationForm(data)
		self.assertFalse(form.is_valid())
		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), data = data)
		request.user = self.user
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		self.assertContains(response, 'Enter a valid date.')
		
	def test_add_reservation_with_idate_after_fdate(self):
		idate_after_fdate = datetime.now().date() + timedelta(days = 8)
		valid_fdate = datetime.now().date() + timedelta(days=7)
		data = self.create_res_data(idate_after_fdate, valid_fdate)
		form = ReservationForm(data)
		self.assertFalse(form.is_valid())
		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room.pk)), data = data)
		request.user = self.user
		response = add_reservation(request, self.hotel.pk, self.room.pk)
		self.assertContains(response, 'Initial Date must be earlier than Final Date')
		
	def test_add_reservation_with_date_in_the_past(self):
		past_idate = datetime.now().date() + timedelta(days = -7)
		past_fdate = datetime.now().date() + timedelta(days = -4)
		data = self.create_res_data(past_idate, past_fdate)
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
   		storage = get_messages(request)
   		message = []
   		for mm in storage:
   			message.append(mm)
   		self.assertTrue(self.hotel.pk != self.room2.hotel.pk)
   		self.assertEqual(response.get('location'), reverse('portal:personal'))
   		self.assertEqual(len(message), 1)
   		self.assertEqual(str(message[0]),'This room is not in this Hotel.')
   		#POST
   		data = dict()
   		request = self.factory.post(reverse('reservation:add_reservation', args = (self.hotel.pk, self.room2.pk)), data = data, follow = True)
   		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)
   		request.user = self.user
   		response = add_reservation(request, self.hotel.pk, self.room2.pk)
   		storage = get_messages(request)
   		message = []
   		for mm in storage:
   			message.append(mm)
   		response.client = Client()
   		response.client.login(username='prova', password='prova')
   		self.assertTrue(self.hotel.pk != self.room2.hotel.pk)
   		self.assertEqual(response.get('location'), reverse('portal:personal'))
   		self.assertEqual(len(message), 1)
   		self.assertEqual(str(message[0]),'This room is not in this Hotel.')
