__author__ = 'federico'
from uploader.models import Upload
from django import forms

# FileUpload form class.
class UploadForm(forms.ModelForm):
    hostname = forms.CharField(
        label='Server Name',
        max_length=50,
        required=False
    )

    class Meta:
        model = Upload
        fields = "__all__"
