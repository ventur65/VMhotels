from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from registration.views import RegistrationView as BaseRegistrationView
from registration import signals
from hotels.models import Hotel
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

# Create your views here.
@login_required
def portal_welcome(request):
	"""
	If users are authenticated, direct them to the portal welcome page
	(template index.html). Otherwise, take them to the login page.
	"""
	return render(request, 'portal/index.html', {'request': request})

@login_required
def personal(request):
	user = request.user
	hotel_list = Hotel.objects.filter(user=user)
	return render(request, 'portal/personal.html', {'request': request, 'hotel_list': hotel_list})
	
@login_required
def upload(request):
    if 'Ok' in request.POST:
    	u = request.user
    	form = UserForm(request.POST, instance=u)
    	if form.is_valid():
    		form.save()
		return HttpResponseRedirect(reverse('portal:personal'))
    elif request.method == 'GET': ##caso GET
    	u = request.user
    	form = UserForm(instance = u)
    return render(request, 'portal/upload.html', {'form' : form})
    
def logout_view(request):
	"Log users out and re-direct them to the main page."
	logout(request)
	#return HttpResponseRedirect('/')
	return HttpResponseRedirect(reverse('main_page'))


class RegistrationView(BaseRegistrationView):
	def register(self, form):
		User = get_user_model()
		new_user = form.save()
		new_user = authenticate(
			username=getattr(new_user, User.USERNAME_FIELD),
			password=form.cleaned_data['password1']
		)
		g = Group.objects.get(name='owners')
		new_user.groups.add(g)
		new_user.user_permissions = [p for p in g.permissions.all()]
		login(self.request, new_user)
		signals.user_registered.send(sender=self.__class__,
									user=new_user,
									request=self.request)
		return new_user

	def get_success_url(self, user):
		return '/'
