__author__ = 'federico'
from django import forms
from .jsongen import getavaliabledatavals

# FileUpload form class.

class downsampling(forms.Form):
    apply_downsampling = forms.BooleanField()
    FS_NEW = forms.IntegerField(required=False)
    #
    # def __init__(self, *args, **kwargs):
    #     nome = kwargs.pop('nome', 'ciao')
    #     super(downsampling, self).__init__(*args, **kwargs)
    #     self.fields['FS_NEW']widget.attrs['name'] = nome



class smoothGaussian(forms.Form):
    apply_smooth = forms.BooleanField()
    sigma = forms.FloatField(min_value=0, required=False)


CHOICES = [("butter", "Butterworth"),
           ("cheby1", "Chebyshev I"),
           ("cheby2", "Chebyshev II"),
           ("ellip", "Couer/Ellip"),
           ("none", "Filter OFF")]


class filterAlg(forms.Form):
    apply_alg_filter = forms.BooleanField()
    passFr = forms.FloatField(min_value=0, required=False)
    stopFr = forms.FloatField(min_value=0, required=False)
    LOSS = forms.FloatField(min_value=0, required=False)
    ATTENUATION = forms.FloatField(min_value=0, required=False)
    filterType = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=False)


class remove_spike(forms.Form):
    apply_spike = forms.BooleanField()
    TH = forms.FloatField(min_value=0, required=False)


class GSR_Form(forms.Form):
    T1 = forms.FloatField(min_value=0.0)
    T2 = forms.FloatField(min_value=0.0)
    MX = forms.FloatField(min_value=0.0)
    DELTA_PEAK = forms.FloatField(min_value=0)
    k_near = forms.IntegerField(min_value=0)
    grid_size = forms.IntegerField(min_value=0)
    s = forms.FloatField(min_value=0)


class EKG_Form(forms.Form):
    delta = forms.FloatField(min_value=0)
    minFr = forms.FloatField(min_value=0)
    maxFr = forms.FloatField(min_value=0)


class BVP_Form(forms.Form):# Uguale a quello sopra ma cambia un default
    delta = forms.FloatField(min_value=0)
    minFr = forms.FloatField(min_value=0)
    maxFr = forms.FloatField(min_value=0)


class Inertial_Form(forms.Form):
    coeffAcc = forms.FloatField(min_value=0)
    coeffGyr = forms.FloatField(min_value=0)
    coeffMag = forms.FloatField(min_value=0)



class choose_exp(forms.Form):
    experiment = forms.ChoiceField()
    asd = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(choose_exp, self).__init__(*args, **kwargs)
        print get_my_choices()
        self.fields['experiment'].choices = get_my_choices()
        self.fields['asd'].choices = [('ciao', 'Hello')]


class lineinout(forms.Form):
    lines = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(linein, self).__init__(*args, **kwargs)
        self.fields['lines'].choices = get_my_choices()


class windowing(forms.Form):
    get_windows = forms.ChoiceField(choices=['get windows contiguous', 'get windows no mix', 'get windows full label'])
    wlen = forms.IntegerField(min_value=0)
    wstep = forms.IntegerField(min_value=0)


