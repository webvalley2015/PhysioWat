from django import forms
from django.forms import ModelForm
from PhysioWat.models import Experiment

# FileUpload form class.
class experiments(ModelForm):
    name = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.Textarea())
    token = forms.CharField(widget=forms.PasswordInput())
    repeat_token = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Experiment
        fields = ['name', 'description', 'token']

