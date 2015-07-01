__author__ = 'federico'
#from uploader.models import Upload
from django import forms

# FileUpload form class.
class UploadForm(forms.Form):
    file = forms.FileField()
