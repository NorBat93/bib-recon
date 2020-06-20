# forms.py 
from django import forms 
from .models import *

class PhotoForm(forms.Form): 
    zawody = forms.ModelChoiceField(
        queryset=Competitions.objects.all(),  to_field_name="comp_slug")
    file_field = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class SearchForm(forms.Form):
    zawody = forms.ModelChoiceField(
        queryset=Competitions.objects.filter(status="published"),  to_field_name="comp_slug")
    numer = forms.DecimalField(decimal_places=0)


class ChangeForm(forms.Form):
    zawody = forms.ModelChoiceField(
        queryset=Competitions.objects.all(),  to_field_name="comp_slug")


class ChangeIDForm(forms.Form):
    numerki = forms.CharField()
