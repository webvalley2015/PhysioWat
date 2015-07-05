__author__ = 'federico'
#from uploader.models import Upload
from django import forms

# FileUpload form class.
class UploadForm(forms.Form):
    #device = forms.CharField()
    file = forms.FileField()
    device = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Device - Max Character Length: 50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Device Description - Max Character Length: 200'}),  max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())
