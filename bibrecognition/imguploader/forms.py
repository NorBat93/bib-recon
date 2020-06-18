# forms.py 
from django import forms 
from .models import *

class PhotoForm(forms.Form): 
    zawody = forms.ModelChoiceField(
        queryset=Competitions.objects.all(),  to_field_name="comp_slug")
    file_field = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
