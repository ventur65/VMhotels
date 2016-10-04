from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
@login_required
def portal_welcome(request):
	"""
	If users are authenticated, direct them to the portal welcome page
	(template index.html). Otherwise, take them to the login page.
	"""
	return render(request, 'portal/index.html', {'request': request})
	
@login_required
def upload(request):
    if 'Ok' in request.POST:
    	u = request.user
    	form = UserForm(request.POST, instance=u)
    	if form.is_valid():
    		form.save()
		return HttpResponse('Dati aggiornati')
    elif 'Cancel' in request.POST:
    	return HttpResponseRedirect("/portal/")
    elif request.method == 'GET': ##caso GET
    	u = request.user
    	form = UserForm(instance = u)
    return render(request, 'portal/upload.html', {'form' : form})
