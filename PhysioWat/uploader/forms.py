__author__ = 'federico'
# from uploader.models import Upload
from django import forms
import os

# FileUpload form class.
class UploadForm(forms.Form):
    # device = forms.CharField()
    file = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))
    device = forms.CharField(widget=forms.TextInput(), max_length=50)
    description = forms.CharField(widget=forms.Textarea(), max_length=200)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50)




