from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from hotels.models import Room, Hotel
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.views import generic
# Create your views here.

@login_required
def add_review(request, hotel_id):
	h = get_object_or_404(Hotel, pk=hotel_id)
	
	rev_list = Review.objects.filter(hotel=hotel_id)
	
	if 'Ok' in request.POST:
		form = ReviewForm(request.POST)
		if form.is_valid():
			newrev = form.save(commit=False)
			newrev.user = request.user
			newrev.hotel = h
			newrev.save()
			h.save()
			return HttpResponse("Commento inserito con successo")
		else:
			return HttpResponse("Commento non valido")
	else:
		form = ReviewForm()
	return render(request, 'review/addcomment.html', {'form': form, 'hotel': h, 'rev_list': rev_list})
