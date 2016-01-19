from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login as django_login

# Create your views here.

def persona_login(request):
	user = authenticate(assertion=request.POST['assertion'])
	if user:
		django_login(request, user)
	return HttpResponse('OK')