__author__ = 'federico'
#from uploader.models import Upload
from django import forms

# FileUpload form class.
class UploadForm(forms.Form):
    device = forms.CharField()
    file = forms.FileField()
    password = forms.CharField(widget=forms.PasswordInput())
