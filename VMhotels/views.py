from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from .forms import RegisterForm
from registration import signals
from registration.views import RegistrationView as BaseRegistrationView
from django.shortcuts import render_to_response
from django.template import RequestContext
from hotels.models import Hotel

User = get_user_model()

def main_page(request):
    query_string = ''
    found_entries = None
    search_fields=('uid')
    
    if ('q' in request.GET) and request.GET['q'].strip() and ('search' in request.GET):

        query_string = request.GET['q']

        found_entries = Hotel.objects.filter(city=query_string)
	return render_to_response('search.html',{ 'query_string': query_string, 'found_entries': found_entries },  context_instance=RequestContext(request))
    else:
	return render(request, 'index.html')

def logout_view(request):
	"Log users out and re-direct them to the main page."
	logout(request)
	return HttpResponseRedirect('/')
	
class RegistrationView(BaseRegistrationView):
	def register(self, form):
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

##NON SERVE PIU'
def register_view(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			#user = form.save(commit = False) ##METTERE TRY
			#print form.fields['password']
			#user.set_password(str(form.fields['password']))
			#user.save()
			g = Group.objects.get(name='owners')
			user.groups.add(g)
			user.user_permissions = [p for p in g.permissions.all()]
			return HttpResponseRedirect('/login')
	else:
		form = RegisterForm()
	return render(request, 'registration.html', {'form': form})

