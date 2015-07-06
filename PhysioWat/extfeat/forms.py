from django import forms
#from preproc.jsongen import getavaliabledatavals

class windowing(forms.Form):
    my_choiches= [('contigous','continous windowing'), ('no_mix','not mixed windowing'), ('full_label','full label windowing')]
    type = forms.ChoiceField(choices=my_choiches, widget=forms.RadioSelect())
    length = forms.FloatField(min_value=0.000001)
    step = forms.FloatField(min_value=0.000001)