from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views import generic
from .models import Room, Hotel
from .forms import HotelForm, RoomForm
from django import forms
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
class HotelDetailView(generic.DetailView):
	model = Hotel
	template_name = 'hotels/hotel_detail.html'
	
def room_detail(request, hotel_id, room_id):
	hotel = get_object_or_404(Hotel, pk=hotel_id)
	room = get_object_or_404(Room, pk=room_id)
	context = {'hotel': hotel, 'room': room}
	return render(request, 'hotels/room_detail.html', context)

@login_required
@permission_required('hotels.add_hotel')
def create_hotel(request):
	if request.method == 'POST':
		form = HotelForm(request.POST, request.FILES)
		if form.is_valid():
			h = form.save(commit=False)
			h.user = request.user
			h.save() ##FARE CON TRY-CATCH
			return HttpResponseRedirect("/hotels/"+str(h.id))
	else:
		form = HotelForm()
	return render(request, 'hotels/inserthotel.html', {'form': form,})

@login_required
@permission_required('hotels.add_room')
def create_room(request, hotel_id):
	if request.method == 'POST':
		h = get_object_or_404(Hotel, pk=hotel_id)
		if request.user == h.user:
			form = RoomForm(request.POST, request.FILES)
			if form.is_valid():
				r = form.save(commit = False)
				r.hotel = h
				r.save() ##FARE CON TRY-CATCH
				return HttpResponseRedirect('/'.join(['/hotels', str(h.pk), str(r.pk)]))
		else: #Caso di user non uguale
			HttpResponseForbidden("You can't add a room to an hotel not yours.")
	else: #caso GET
		form = RoomForm()
	return render(request, 'hotels/insertroom.html', {'form': form,})

@login_required
@permission_required('hotels.change_hotel')
def edit_hotel(request, hotel_id):
	h = get_object_or_404(Hotel, pk=hotel_id)
	if request.user != h.user: ##Se l'utente della sessione non e' il proprietario dell'hotel
		#logout(request)
		#return HttpResponseRedirect("/login")
		return HttpResponseForbidden("You can't edit an hotel not yours.")
	if 'Ok' in request.POST:
		form = HotelForm(request.POST, request.FILES, instance = h)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/hotels/"+str(h.pk))
	elif 'Cancel' in request.POST:
		return HttpResponseRedirect("/hotels/"+str(h.pk))
	elif request.method == 'GET': ##caso GET
		form = HotelForm(instance = h)
	return render(request, 'hotels/edithotel.html', {'form': form, 'hotel': h}) 
    	
@login_required
@permission_required('hotels.change_room')	
def edit_room(request, hotel_id, room_id):
	h = get_object_or_404(Hotel, pk=hotel_id)
	r = get_object_or_404(Room, pk=room_id)
	if h.user != request.user: ##Se l'utente della sessione non e' il proprietario dell'hotel
		return HttpResponseForbidden("You can't edit a room of an hotel not yours")
	if h.pk == r.hotel.pk: ##Se la stanza e' di questo hotel
		if 'Ok' in request.POST:
			form = RoomForm(request.POST, request.FILES, instance = r)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/'.join(["/hotels",str(h.id),str(r.id)]))
		elif 'Cancel' in request.POST:
			return HttpResponseRedirect("/hotels/"+str(h.pk)+"/"+str(r.pk))
		elif request.method == 'GET': ##caso GET
			form = RoomForm(instance = r)
		return render(request, 'hotels/editroom.html', {'form': form, 'hotel': h, 'room': r})
	return HttpResponse("This room doesn't exist in this Hotel")
			
			
			
	
	
	
	
