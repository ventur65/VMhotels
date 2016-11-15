from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from hotels.models import Room, Hotel
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from .models import Reservation
from .views import *
from .forms import ReservationForm
from django.test.client import Client
from .urls import *
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest
import requests

#def create_reserv (ffdate):
#	"""
#	 Creates a reservation that controls the start date and the end date
# 	"""
# 	iidate = datetime.today()
# 	user_id = User.objects.create_user('prova', 'prova@prova.com')
# 	hotel_id = Hotel.objects.create(user=user_id)
# 	room_id = Room.objects.create (hotel=hotel_id, number=1, cost=1)
# 	Reservation.objects.create(user=user_id, idate=iidate, fdate=ffdate, room=room_id, is_active=True)
#	return iidate
	
class AddReservationViewTests(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		
	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create_user(username='prova', email='ciao@mail.it', password='prova')
		new_group, created = Group.objects.get_or_create(name='customers')
		ct = ContentType.objects.get_for_model(Reservation)
		permissions = Permission.objects.get(codename="add_reservation")
		new_group.permissions.add(permission)
		cls.user.groups.add(new_group)
		cls.user.user_permissions = [permission]
		cls.hotel = Hotel.objects.create(name = 'ciao')
		cls.room = Room.objects.create(hotel=cls.hotel, number = 1, cost = 1)
		iidate = datetime.now().date()
		ffdate = datetime.now().date() + timedelta(days=7)
		cls.res = Reservation.objects.create(user = cls.user, idate = iidate, fdate = ffdate, room = cls.room, firstname = 'giovanni', is_active = True)
		
	def test_add_reservation_view_with_wrong_date(self):
		self.client.login(username='prova', password='prova')
    	self.client.get(reverse('reservation:add_reservation'))
    	self.assertEqual(response.status_code, 200)
    	
   	def test_res_with_fdate_in_past(self):
   		fdate = self.res.fdate
		idate = self.res.idate
		self.assertFalse(idate < fdate)	
#    def test_res_with_same_idate(self):
#    	iidate = self.res.idate
#    	ffdate = self.res.fdate
#    	uprova = User.objects.create_user(username='Giova', email='gio@mail.it')
#    	instance = Reservation.objects.create(user=uprova, idate=iidate, fdate=ffdate, room=self.room, is_active=True, tel='+393335661378')
#    	self.assertTrue(check_res(instance,self.room))
#    	
#    def test_add_reservation(self):    	
#    	iidate = datetime.now().date() + timedelta(days=10)
#	ffdate = datetime.now().date() + timedelta(days=18)   	
#	
#	#request = self.c.post("/reservation/"+str(self.hotel.id)+"/"+str(self.room.id)+"/add/", {'firstname': 'john', 'lastname': 'prov', 'idate': iidate, 'fdate': ffdate, 'city': 'fabbrico', 'address': 'ciao', 'email': 'prova@gmail.com', 'tel': '+393335661379'}, follow=True)
#	
#	session = requests.Session()
#	
#	data= {
#    		'firstname': 'john',
#    		'lastname': 'prov',
#    		'idate': iidate,
#    		'fdate': ffdate,
#    		'city': 'fabbrico',
#    		'address': 'ciao',
#    		'email': 'prova@gmail.com',
#    		'tel': '+393335661379',
#    		'login': 'prova',
#    		'password': 'prova',
#    	}
#    	
#    	session.user = self.user
#    	permissions = Permission.objects.filter(user=self.user)
#    	print permissions 
#    	response = session.post('http://127.0.0.1:8000/reservation/'+str(self.hotel.id)+'/'+str(self.room.id)+'/add/', data=data)
#	
#	#r = requests.post('http://127.0.0.1:8000/reservation/'+str(self.hotel.id)+'/'+str(self.room.id)+'/add/', data=data, auth=('prova', 'prova'))
#	#r.user = self.user
#	print response.status_code 
#	
#	#request.user = self.user
#	
#	#response = add_reservation(request, self.hotel.id, self.room.id)
#	
#	#print Reservation.objects.get(idate= iidate) #dalla stampa degli oggetti resetvation non ritorna la reservation creata la riga prima con la post
#	
#	self.assertEqual(response.status_code, 302)    
#           	
#        	