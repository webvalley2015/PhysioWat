from django.test import TestCase
from PhysioWat.models import Experiment
# Create your tests here.
def getExperimentsTouple():
    list = Experiment.objects.values_list('id', 'name', flat=True).distinct()
    print list