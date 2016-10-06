from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from hotels.models import Room, Hotel
from .models import Reservation
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.views import generic
# Create your views here.

##NON E' UNA VIEW.
def check_res(newres, room):
	for res in Reservation.objects.filter(room = room):
		if (newres.idate >= res.idate) and (newres.idate <= res.fdate):
			return False
		elif (newres.fdate >= res.idate) and (newres.fdate <= res.fdate):
			return False
		elif (newres.idate >= res.idate) and (newres.fdate <= res.fdate):
			return False
		elif (newres.idate <= res.idate) and (newres.fdate >= res.fdate):
			return False
	return True	

@login_required
@permission_required('reservation.add_reservation')
def add_reservation(request, hotel_id, room_id):
	h = get_object_or_404(Hotel, pk=hotel_id)
	r = get_object_or_404(Room, pk=room_id)
	if h.pk != r.hotel.pk:
		return HttpResponse("Non esiste questa stanza in questo Hotel")
	if 'Ok' in request.POST:
		form = ReservationForm(request.POST)
		if form.is_valid():
			newres = form.save(commit=False)
			if check_res(newres, r):
				newres.user = request.user
				newres.room = r
				newres.save()
				r.save()
				return HttpResponse("Stanza Riservata con Successo")
			else:
				return HttpResponse("Stanza gia prenotata in quel periodo")
	else:
		form = ReservationForm()
	return render(request, 'reservation/addreservation.html', {'form': form, 'hotel': h, 'room': r})

@login_required
def reservation_detail(request, reservation_id):
	res = get_object_or_404(Reservation, pk=reservation_id)
	if request.user == res.user:
		return render(request, 'reservation/reservation_detail.html', {'reservation': res})
	return HttpResponse("NON SEI L'UTENTE CHE HA EFFETTUATO QUESTA PRENOTAZIONE")
	
	
	
	
