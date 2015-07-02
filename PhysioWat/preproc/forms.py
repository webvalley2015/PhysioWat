__author__ = 'federico'
from django import forms

# FileUpload form class.
class PreprocSettings(forms.Form):
    file = forms.SelectMultiple()

