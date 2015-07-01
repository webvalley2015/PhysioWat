__author__ = 'federico'
from uploader.models import Upload
from django import forms

# FileUpload form class.
class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = "__all__"
