__author__ = 'stephen'

from django import forms

# FileUpload form class.
class SensorDesignerForm(forms.Form):
    Name = forms.CharField()
    Sensors = forms.IntegerField(min_value=1)

