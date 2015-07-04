__author__ = 'stephen'

from django import forms

# FileUpload form class.
class SensorDesignerForm(forms.Form):
    Name = forms.CharField()
    Sensors = forms.IntegerField(min_value=1, max_value=25, widget=forms.NumberInput(attrs={
        'onClick': "getValue()",
    }))

class experiments(forms.Form):
    name = forms.CharField()
    desc = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

