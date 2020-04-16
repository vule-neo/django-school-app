from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.utils.translation import gettext_lazy as _


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

class UploadFileForm(forms.ModelForm):
	class Meta:
		model = FileUpload
		fields = ["text", "file", ]