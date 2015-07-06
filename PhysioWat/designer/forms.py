from django import forms
from django.forms import ModelForm
from PhysioWat.models import Experiment

# FileUpload form class.
class experiments(ModelForm):
    name = forms.CharField(widget=forms.TextInput(), max_length=50)
    description = forms.CharField(widget=forms.Textarea(), max_length=500)
    token = forms.CharField(widget=forms.PasswordInput(), max_length=50)
    repeat_token = forms.CharField(widget=forms.PasswordInput(), max_length=50)
    class Meta:
        model = Experiment
        fields = ['name', 'description', 'token']

