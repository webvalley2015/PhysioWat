from django import forms
#from preproc.jsongen import getavaliabledatavals

class windowing(forms.Form):
    my_choices= [('contigous','continous windowing'), ('no_mix','not mixed windowing'), ('full_label','full label windowing')]
    type = forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect())
    length = forms.FloatField(min_value=0.000001)
    step = forms.FloatField(min_value=0.000001)

class viewFeatures(forms.Form):
    my_choices = [('norm','normalize features'), ('sel','select features') ]
    viewf = forms.ChoiceField(choices=my_choices,widget=forms.CheckboxSelectMultiple())

class FeatPar(forms.Form):
     my_choices =[('k_selected','Select the number of features'),('k_auto', 'Automatic number of features')]
     FeatChoose = forms.ChoiceField(choices=my_choices,widget=forms.RadioSelect())
     feat_num = forms.IntegerField(min_value=0)

class TestParam(forms.Form):
    test_percentage = forms.FloatField(min_value=1)
    number_of_iterations = forms.IntegerField(min_value=1)

class AlgChoose(forms.Form):
    my_choices = [('knear','k nearest'),('svm', 'support vector machine'),('dectree','decison tree'),
                  ('rndfor','random forest'),('adaboost','ada boost'),('lda','latent direct assocation'),
                  ('quad_disc','quadratic discriminant analisys')]
    alg_choice= forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect())


class AlgParam (forms.Form):
    my_choices = [('def','default parameters'),('auto','autofit'),('pers','define parameters')]
    parameter_choiche = forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect())

class SvmParam(forms.Form):
    my_choices=[('linear','linear'),('rbf','rbf'),('sigmoid','sigmoid')]
    kernel = forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect())
    C = forms.IntegerField(min_value=1)

class KNearParam(forms.Form):
    k_neighbour = forms.IntegerField(min_value=1)

class DecTreeParam(forms.Form):
    max_features = forms.IntegerField(min_value=1)

class RndForParam(forms.Form):
    my_choices=[('1','1'),('None','None'),('sqrt','square root'),('log2','log 2')]
    max_features = forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect())
    number_estimators = forms.IntegerField(min_value=1)

class AdaBoostParam(forms.Form):
    number_estimators = forms.IntegerField(min_value=1)
    learning_rate = forms.FloatField(min_value=0.25)

class LatDirAssParam(forms.Form):
    my_choices=[('svd','svd'),('lsqr','lsqr'),('eigen','eigen')]
    solver = forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect())

class autoFitParam(forms.Form):
    my_choices= [('a','a'),('v','v'),('c','c')]
    maxmimize = forms.ChoiceField(choices=my_choices,widget=forms.RadioSelect())