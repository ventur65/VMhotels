from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Room, Hotel
from .forms import HotelForm, RoomForm
from django import forms
from django.contrib.auth.decorators import login_required

# Create your views here.
class HotelDetailView(generic.DetailView):
	model = Hotel
	template_name = 'hotels/hotel_detail.html'
	
def room_detail(request, hotel_id, room_id):
	hotel = get_object_or_404(Hotel, pk=hotel_id)
	room = get_object_or_404(Room, pk=room_id)
	context = {'hotel': hotel, 'room': room}
	return render(request, 'hotels/room_detail.html', context)

@login_required()
def create_hotel(request):
	if request.method == 'POST':
		form = HotelForm(request.POST, request.FILES)
		if form.is_valid():
			h = form.save(commit=False)
			h.user = request.user
			h.save()
			return HttpResponseRedirect("/hotels/"+str(h.id))
	else:
		form = HotelForm()
	return render(request, 'hotels/inserthotel.html', {'form': form,})

@login_required()
def create_room(request, hotel_id):
	if request.method == 'POST':
		h = get_object_or_404(Hotel, pk=hotel_id)
		if request.user == h.user:
			form = RoomForm(request.POST, request.FILES)
			if form.is_valid():
				r = form.save(commit = False)
				r.hotel = h
				r.save()
				return HttpResponseRedirect('/'.join(['/hotels', str(h.pk), str(r.pk)]))
		else: #Caso di user non uguale
			HttpResponse("Non sei il proprietario dell'hotel.")
	else: #caso GET
		form = RoomForm()
	return render(request, 'hotels/insertroom.html', {'form': form,})
			
			
			
	
	
	
	
