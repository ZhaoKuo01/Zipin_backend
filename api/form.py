from django import forms
from .models import *

class Imageform(forms.ModelForm):
    class Meta:
        model = NoteImage
        fields = ['note','image']