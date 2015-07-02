__author__ = 'federico'
from django import forms

# FileUpload form class.


class downsampling(forms.Form):
    FS_NEW = forms.IntegerField()
    switch = forms.BooleanField()

CHOICES=[("butter", "Butterworth"),
        ("cheby1", "Chebyshev I"),
        ("cheby2", "Chebyshev II"),
        ("ellip", "Couer/Ellip"),
        ("none", "Filter OFF")]

class filter(forms.Form):
    passFr = forms.FloatField(min_value = 0)
    stopFr = forms.FloatField(min_value = 0)
    LOSS = forms.FloatField(min_value = 0)
    ATTENUATION = forms.FloatField(min_value = 0)
    filterType = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

class remove_spike(forms.Form):
    remove_spike = forms.BooleanField()
    TH = forms.FloatField(min_value = 0)

class GSR(forms.Form):
    T1 = forms.FloatField(min_value = 0, default = 0.75)
    T2 = forms.FloatField(min_value = 0, default = 2)
    MX = forms.FloatField(min_value = 0, default = 1)
    DELTA_PEAK = forms.FloatField(min_value = 0, default = 0.02)
    k_near = forms.IntegerField(min_value = 0, default = 5)
    grid_size = forms.IntegerField(min_value = 0, default = 5)
    s = forms.FloatField(min_value = 0, default = 0.2)

class EKG(forms.Form):
    delta = forms.FloatField(min_value = 0, default = 0.2)
    minFr = forms.FloatField(min_value = 0, default = 40)
    maxFr = forms.FloatField(min_value = 0, default = 200)

class BVP(forms.Form):  #Uguale a quello sopra ma cambia un default
    delta = forms.FloatField(min_value = 0, default = 1)
    minFr = forms.FloatField(min_value = 0, default = 40)
    maxFr = forms.FloatField(min_value = 0, default = 200)

class inertial(forms.Form):
    coeff = forms.FloatField(default = 1)



