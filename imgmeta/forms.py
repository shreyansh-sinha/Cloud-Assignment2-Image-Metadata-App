from django.forms import ModelForm
from django import forms
from .models import *

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageSet
        fields = ('image',)
        help_texts = {
            'image': None,
        }

class SearchForm(forms.Form):
     searchtext = forms.CharField(max_length=140,widget=forms.Textarea(attrs={'rows':'5', }),label="Search Text")