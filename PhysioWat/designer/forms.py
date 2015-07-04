__author__ = 'stephen'
from django import forms
from django.forms import ModelForm
from PhysioWat.models import PhysiowatExperiment

# FileUpload form class.
class SensorDesignerForm(forms.Form):
    Name = forms.CharField()
    Sensors = forms.IntegerField(min_value=1, max_value=25, widget=forms.NumberInput(attrs={
        'onClick': "getValue()",
    }))

class experiments(ModelForm):
    name = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.Textarea())
    token = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = PhysiowatExperiment
        fields = ['name', 'description', 'token']

