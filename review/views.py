from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from hotels.models import Room, Hotel
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.views import generic
from django.db.models import Avg
# Create your views here.

@login_required
def add_review(request, hotel_id):
	h = get_object_or_404(Hotel, pk=hotel_id)
	if 'Ok' in request.POST:
		form = ReviewForm(request.POST)
		if form.is_valid():
			newrev = form.save(commit=False)
			newrev.user = request.user
			newrev.hotel = h
			newrev.save()
			return HttpResponseRedirect(reverse('hotels:hotel_detail', args=(h.pk,)))
		else:
			return HttpResponse("Commento non valido")
	else:
		form = ReviewForm()
	return render(request, 'review/addreview.html', {'form': form, 'hotel': h})

class ReviewListView(generic.list.ListView):
	template_name = 'review/reviewlist.html'
	context_object_name = 'review_list'
	
	def get_queryset(self):
		h_id = self.kwargs['hotel_id']
		h = get_object_or_404(Hotel, pk = h_id)
		return Review.objects.filter(hotel = h).order_by('-created')[:5]
		
	def get_context_data(self, **kwargs):
		context = super(ReviewListView, self).get_context_data(**kwargs)
		h_id = self.kwargs['hotel_id']
		h = get_object_or_404(Hotel, pk = h_id)
		context['hotel'] = h
		av = Review.objects.filter(hotel=h).aggregate(Avg('rate'))
		context['average'] = av['rate__avg']
		return context

