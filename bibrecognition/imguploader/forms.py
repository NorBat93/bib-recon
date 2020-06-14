# forms.py 
from django import forms 
from .models import *

class PhotoForm(forms.Form): 
    zawody = forms.CharField(max_length=50)
    file_field = forms.FileField(widget=forms.ClearableFileInput())
