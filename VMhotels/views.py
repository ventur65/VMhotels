from django.shortcuts import render
from django.http import HttpResponseRedirect
from hotels.models import Hotel, Room
from review.models import Review
from .forms import SearchForm
from datetime import datetime
from django.db.models import Avg, Min, Max
from django.core.urlresolvers import reverse

def main_page(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			dest = form.cleaned_data['dest']
			beds = form.cleaned_data['beds']
			check_in = form.cleaned_data['checkin']
			check_out = form.cleaned_data['checkout']
			days = check_out - check_in
			rl = dict()
			s = dict()
			found_entries = Hotel.objects.filter(city=dest, room__beds=beds).distinct()
			if form.cleaned_data['rate']:
				found_entries = found_entries.annotate(average=Avg('review__rate')).order_by('-average')
			else:
				#found_entries = found_entries.annotate(average=Avg('room__cost')).order_by('average')
				found_entries = found_entries.order_by('room__cost')
			for h in found_entries:
				rl[h] = h.room_set.filter(beds=beds).aggregate(costmin=Min('cost')*days.days, costmax=Max('cost')*days.days)
				s[h] = h.services.all()
			return render(request, 'search.html', {'found_entries': found_entries, 'days': days.days, 'rl': rl, 's': s})
	elif request.method == 'GET':
		form = SearchForm()
	return render(request, 'index.html', {'form': form})
