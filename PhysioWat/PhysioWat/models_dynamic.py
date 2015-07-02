#auto generated dont touch servers will catch fire
from django.db import models
__author__ = 'andrew'


class ACCX(models.Model):
    experimenterid = models.IntegerField(db_column='ExperimenterID')  # Field name made lowercase.
    experimentid = models.IntegerField(db_column='ExperimentID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='SubjectID')  # Field name made lowercase.
    timestamp = models.FloatField(db_column='TS', primary_key=True)  # Field name made lowercase.
    paramatervalue = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'accx'
        unique_together = (('experimenterid', 'experimentid', 'timestamp', 'subjectid'),)

class ACCY(models.Model):
    experimenterid = models.IntegerField(db_column='ExperimenterID')  # Field name made lowercase.
    experimentid = models.IntegerField(db_column='ExperimentID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='SubjectID')  # Field name made lowercase.
    timestamp = models.FloatField(db_column='TS', primary_key=True)  # Field name made lowercase.
    paramatervalue = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'accy'
        unique_together = (('experimenterid', 'experimentid', 'timestamp', 'subjectid'),)

class ACCZ(models.Model):
    experimenterid = models.IntegerField(db_column='ExperimenterID')  # Field name made lowercase.
    experimentid = models.IntegerField(db_column='ExperimentID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='SubjectID')  # Field name made lowercase.
    timestamp = models.FloatField(db_column='TS', primary_key=True)  # Field name made lowercase.
    paramatervalue = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'accz'
        unique_together = (('experimenterid', 'experimentid', 'timestamp', 'subjectid'),)

class GYROX(models.Model):
    experimenterid = models.IntegerField(db_column='ExperimenterID')  # Field name made lowercase.
    experimentid = models.IntegerField(db_column='ExperimentID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='SubjectID')  # Field name made lowercase.
    timestamp = models.FloatField(db_column='TS', primary_key=True)  # Field name made lowercase.
    paramatervalue = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'gyrox'
        unique_together = (('experimenterid', 'experimentid', 'timestamp', 'subjectid'),)

class GYROY(models.Model):
    experimenterid = models.IntegerField(db_column='ExperimenterID')  # Field name made lowercase.
    experimentid = models.IntegerField(db_column='ExperimentID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='SubjectID')  # Field name made lowercase.
    timestamp = models.FloatField(db_column='TS', primary_key=True)  # Field name made lowercase.
    paramatervalue = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'gyroy'
        unique_together = (('experimenterid', 'experimentid', 'timestamp', 'subjectid'),)

class GYROZ(models.Model):
    experimenterid = models.IntegerField(db_column='ExperimenterID')  # Field name made lowercase.
    experimentid = models.IntegerField(db_column='ExperimentID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='SubjectID')  # Field name made lowercase.
    timestamp = models.FloatField(db_column='TS', primary_key=True)  # Field name made lowercase.
    paramatervalue = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'gyroz'
        unique_together = (('experimenterid', 'experimentid', 'timestamp', 'subjectid'),)

class MAGX(models.Model):
    experimenterid = models.IntegerField(db_column='ExperimenterID')  # Field name made lowercase.
    experimentid = models.IntegerField(db_column='ExperimentID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='SubjectID')  # Field name made lowercase.
    timestamp = models.FloatField(db_column='TS', primary_key=True)  # Field name made lowercase.
    paramatervalue = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'magx'
        unique_together = (('experimenterid', 'experimentid', 'timestamp', 'subjectid'),)

class MAGY(models.Model):
    experimenterid = models.IntegerField(db_column='ExperimenterID')  # Field name made lowercase.
    experimentid = models.IntegerField(db_column='ExperimentID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='SubjectID')  # Field name made lowercase.
    timestamp = models.FloatField(db_column='TS', primary_key=True)  # Field name made lowercase.
    paramatervalue = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'magy'
        unique_together = (('experimenterid', 'experimentid', 'timestamp', 'subjectid'),)

class MAGZ(models.Model):
    experimenterid = models.IntegerField(db_column='ExperimenterID')  # Field name made lowercase.
    experimentid = models.IntegerField(db_column='ExperimentID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='SubjectID')  # Field name made lowercase.
    timestamp = models.FloatField(db_column='TS', primary_key=True)  # Field name made lowercase.
    paramatervalue = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'magz'
        unique_together = (('experimenterid', 'experimentid', 'timestamp', 'subjectid'),)
