from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from hotels.models import Room, Hotel
from .models import Reservation
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.

##NON E' UNA VIEW.
def check_res(newres, room):
	for res in Reservation.objects.filter(room = room, is_active=True):
		if (res == newres):
			continue
		if res.idate <= newres.idate <= res.fdate:
			return False
		elif res.idate <= newres.fdate <= res.fdate:
			return False
		elif (newres.idate >= res.idate) and (newres.fdate <= res.fdate):
			return False
		elif (newres.idate <= res.idate) and (newres.fdate >= res.fdate):
			return False
	return True
	
def update_state_res(room):
	rlist = room.reservation_set.filter(is_active = False).order_by('updated')
	for non_active_res in rlist:
		if check_res(non_active_res, room):
			non_active_res.is_active = True
			non_active_res.save()
			subject = 'Reservation VMHotels'
			mex = "Your reservation for Room " + str(non_active_res.room.number) + " Hotel "+ non_active_res.room.hotel.name + " from " + str(non_active_res.idate) + " to " + str(non_active_res.fdate) + " is now valid."
			frommail = 'progettovmhotels@gmail.com'
			to = [non_active_res.email]
			send_mail(subject, mex, frommail, to, fail_silently = False)

@login_required
@permission_required('reservation.add_reservation')
def add_reservation(request, hotel_id, room_id):
	h = get_object_or_404(Hotel, pk=hotel_id)
	r = get_object_or_404(Room, pk=room_id)
	if h.pk != r.hotel.pk:
		messages.add_message(request, messages.WARNING, 'This room is not in this Hotel.')
		return HttpResponseRedirect(reverse('portal:personal'))
		#return HttpResponseForbidden("Non esiste questa stanza in questo Hotel")
	if 'Ok' in request.POST:
		form = ReservationForm(request.POST)
		if form.is_valid():
			newres = form.save(commit=False)
			newres.user = request.user
			newres.room = r
			if check_res(newres, r):
				newres.is_active = True
				newres.save()
				messages.add_message(request, messages.INFO, 'The reservation is successfully added.')
				return HttpResponseRedirect(reverse('portal:personal'))
			else:
				newres.is_active = False
				newres.save()
				messages.add_message(request, messages.WARNING, 'Your reservation has been added to a queue: if the previous reservations are deleted, you will receive an email.')
				#return render(request, 'reservation/inqueue.html')
				return HttpResponseRedirect(reverse('portal:personal'))
	elif request.method == 'GET':
		form = ReservationForm()
	return render(request, 'reservation/addreservation.html', {'form': form, 'hotel': h, 'room': r})

@login_required
def reservation_detail(request, reservation_id):
	res = get_object_or_404(Reservation, pk=reservation_id)
	if request.user == res.user:
		return render(request, 'reservation/reservation_detail.html', {'reservation': res})
	messages.add_message(request, messages.WARNING, 'The reservation is not yours.')
	return HttpResponseRedirect(reverse('portal:personal'))
	#return HttpResponseForbidden("This reservation is not yours")
	
@login_required
@permission_required('reservation.change_reservation')
def edit_reservation(request, reservation_id):
	res = get_object_or_404(Reservation, pk=reservation_id)
	r = get_object_or_404(Room, pk=res.room.pk)
	h = get_object_or_404(Hotel, pk=r.hotel.pk)
	if res.user != request.user: ##Se l'utente della sessione non e' il titolare della prenotazione
		messages.add_message(request, messages.WARNING, 'The reservation is not yours.')
		return HttpResponseRedirect(reverse('portal:personal'))
	if 'Ok' in request.POST:
		form = ReservationForm(request.POST, instance = res)
		if form.is_valid():
			form.save(commit=False)
			if check_res(res, r):
				res.is_active = True
				messages.add_message(request, messages.SUCCESS, 'The reservation is successfully changed.')
			else:
				res.is_active = False
				messages.add_message(request, messages.WARNING, 'Reservation changed. Your reservation has been added to a queue: if the previous reservations are deleted, you will receive an email.')
			res.save()
			update_state_res(r)
			return HttpResponseRedirect(reverse('portal:personal'))
	elif request.method == 'GET': ##caso GET
		form = ReservationForm(instance = res)
	return render(request, 'reservation/editreservation.html', {'form': form, 'hotel': h, 'room': r, 'reservation':res,})
	
@login_required
@permission_required('reservation.delete_reservation')
def delete_reservation(request, reservation_id):
	res = get_object_or_404(Reservation, pk=reservation_id)
	r = get_object_or_404(Room, pk=res.room.pk)
	h = get_object_or_404(Hotel, pk=r.hotel.pk)
	if res.user != request.user: ##Se l'utente della sessione non e' il titolare della prenotazione
		messages.add_message(request, messages.WARNING, 'The reservation is not yours.')
		return HttpResponseRedirect(reverse('portal:personal'))
		#return HttpResponseForbidden("This reservation is not yours.")
	if 'Ok' in request.POST:
#		Reservation.objects.filter(id=res.id).delete()
		res.delete()
		update_state_res(r)
		messages.add_message(request, messages.WARNING, 'The reservation is successfully removed.')
		return HttpResponseRedirect(reverse('portal:personal'))
	return render(request, 'reservation/deletereservation.html', {'hotel': h, 'room': r, 'reservation':res,})
