from django import forms
#from preproc.jsongen import getavaliabledatavals

class windowing(forms.Form):
    my_choices= [('contigous','continous windowing'), ('no_mix','not mixed windowing'), ('full_label','full label windowing')]
    type = forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect())
    length = forms.FloatField(min_value=0.00001, initial=1)
    step = forms.FloatField(min_value=0.000001, initial=1)


class viewFeatures(forms.Form):
    my_choices = [('norm','normalize features'), ('sel','select features. if not ticked, immediatly following selector will not be taken in consider') ]
    viewf = forms.ChoiceField(choices=my_choices,widget=forms.CheckboxSelectMultiple())

class FeatPar(forms.Form):
     my_choices =[('k_auto', 'Automatic number of features'),('k_selected','Select the number of features')]
     FeatChoose = forms.ChoiceField(choices=my_choices,widget=forms.RadioSelect(), initial='k_auto')
     feat_num = forms.IntegerField(min_value=0, initial=0)

class TestParam(forms.Form):
    test_percentage = forms.IntegerField(min_value=1, initial=1)
    number_of_iterations = forms.IntegerField(min_value=1, initial=1)

class AlgChoose(forms.Form):
    my_choices = [('KNN','k nearest'),('SVM', 'support vector machine'),('DCT','decison tree'),
                  ('RFC','random forest'),('ADA','adaboost'),('LDA','latent direct assocation'),
                  ('QDA','quadratic discriminant analisys'),('ALL','Try every algorightm. Implies autofit')]
    alg_choice= forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect(), initial='KNN')


class AlgParam (forms.Form):
    my_choices = [('def','default parameters'),('auto', 'automatically find the best fit (might take a long time)'),('pers','define parameters')]
    parameter_choiche = forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect(),initial='auto')

class SvmParam(forms.Form):
    my_choices=[('linear','linear'),('rbf','rbf'),('sigmoid','sigmoid')]
    kernel = forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect(), initial='linear')
    C = forms.IntegerField(min_value=1, initial=10)

class KNearParam(forms.Form):
    k_neighbour = forms.IntegerField(min_value=1, initial=5)

class DecTreeParam(forms.Form):
    my_choices= [('1','1'),('None','None'),('sqrt','square root'),('log2','log2')]
    max_features = forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect(), initial='1')

class RndForParam(forms.Form):
    my_choices=[('1','1'),('None','None'),('sqrt','square root'),('log2','log 2')]
    max_features = forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect(), initial='1')
    number_estimators = forms.IntegerField(min_value=1, initial=1)

class AdaBoostParam(forms.Form):
    number_estimators = forms.IntegerField(min_value=1, initial=1)
    learning_rate = forms.FloatField(min_value=0.25, initial=1)

class LatDirAssParam(forms.Form):
    my_choices=[('svd','svd'),('lsqr','lsqr'),('eigen','eigen')]
    solver = forms.ChoiceField(choices=my_choices, widget=forms.RadioSelect(), initial='svd')

class autoFitParam(forms.Form):
    my_choices= [('ACC','accuracy %'),('F1M','F-Test macro '),('F1m','F-Test micro'),('F1W','F-Test weighted'),
                 ('WHM','Weighted Harmonic Mean of precision and recall'),('PRM','Precision Score Macro'),
                 ('PRm','Precision Score Micro'), ('PRW','Precision Score Weighted'),
                 ('REM','Recall Score Macro'),('REm','Recall Score Micro'),('REW','Recall Score Weighted')
                 ]
    maximize = forms.ChoiceField(choices=my_choices,widget=forms.RadioSelect(), initial='ACC')

#--------------------------------------------
# todo FORMS FOR FEAT EXTS
#------------------------------------------------

class signal_choose(forms.Form):
    choose_signal = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple(), required=True)

    def __init__(self, choices, *args, **kwargs):
        super(signal_choose,self).__init__(*args, **kwargs)
        self.fields['choose_signal'].choices = choices

#TODO fix item type
class id_choose(forms.Form):
    choose_id = forms.ChoiceField(choices=[], widget=forms.Select())

    def __init__(self, choices, *args, **kwargs):
        super(id_choose,self).__init__(*args, **kwargs)
        self.fields['choose_id'].choices = choices