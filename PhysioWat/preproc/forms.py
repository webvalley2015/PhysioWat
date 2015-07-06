__author__ = 'federico'
from django import forms
from .jsongen import getavaliabledatavals

# FileUpload form class.

class downsampling(forms.Form):
    FS_NEW = forms.IntegerField()
    switch = forms.BooleanField()


class smoothGaussian(forms.Form):
    sigma = forms.FloatField(min_value=0)
    switch = forms.BooleanField()


CHOICES = [("butter", "Butterworth"),
           ("cheby1", "Chebyshev I"),
           ("cheby2", "Chebyshev II"),
           ("ellip", "Couer/Ellip"),
           ("none", "Filter OFF")]


class filterAlg(forms.Form):
    passFr = forms.FloatField(min_value=0)
    stopFr = forms.FloatField(min_value=0)
    LOSS = forms.FloatField(min_value=0)
    ATTENUATION = forms.FloatField(min_value=0)
    filterType = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())


class remove_spike(forms.Form):
    remove_spike = forms.BooleanField()
    TH = forms.FloatField(min_value=0)


class GSR(forms.Form):
    T1 = forms.FloatField(min_value=0.0)
    T2 = forms.FloatField(min_value=0.0)
    MX = forms.FloatField(min_value=0.0)
    DELTA_PEAK = forms.FloatField(min_value=0)
    k_near = forms.IntegerField(min_value=0)
    grid_size = forms.IntegerField(min_value=0)
    s = forms.FloatField(min_value=0)


class EKG(forms.Form):
    delta = forms.FloatField(min_value=0)
    minFr = forms.FloatField(min_value=0)
    maxFr = forms.FloatField(min_value=0)


class BVP(forms.Form):  # Uguale a quello sopra ma cambia un default
    delta = forms.FloatField(min_value=0)
    minFr = forms.FloatField(min_value=0)
    maxFr = forms.FloatField(min_value=0)


class inertial(forms.Form):
    coeff = forms.FloatField(min_value=0)


class choose_exp(forms.Form):
    experiment = forms.ChoiceField()
    asd = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(choose_exp, self).__init__(*args, **kwargs)
        #print get_my_choices()
        self.fields['experiment'].choices = get_my_choices()
        self.fields['asd'].choices = [('ciao', 'Hello')]


class lineinout(forms.Form):
    lines = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(linein, self).__init__(*args, **kwargs)
        self.fields['lines'].choices = get_my_choices()





