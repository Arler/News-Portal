from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
	email = forms.EmailField(label='Email')
	first_name = forms.CharField(label='Имя')
	last_name = forms.CharField(label='Фамилия')

	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',
		)