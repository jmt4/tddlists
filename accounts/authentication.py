import requests

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'

from django.contrib.auth import get_user_model
from django.contrib.auth import models
from django.conf import settings
User = get_user_model()

class PersonaAuthenticationBackend(object):
	
	def authenticate(self, assertion):
		resp = requests.post(
			PERSONA_VERIFY_URL, 
			data={'audience': settings.DOMAIN, 'assertion': assertion}
		)
		
		if resp.ok and resp.json()['status'] == 'okay':
			email=resp.json()['email']
			try:
				return User.objects.get(email=email)
			except User.DoesNotExist:
				return User.objects.create(email=email)

	def get_user(self, email):
		try:
			return User.objects.get(email=email)
		except User.DoesNotExist:
			return None