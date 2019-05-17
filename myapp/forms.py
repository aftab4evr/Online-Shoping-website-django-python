from django import forms
from myapp.models import *

class SingUpForm(forms.ModelForm):
	class Meta:
		# model=SingUp
		fields=("full_name","email","mobile","password")

