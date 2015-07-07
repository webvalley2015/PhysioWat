__author__ = 'andrew'

from PhysioWat.models import Recording,SensorRawData,Preprocessed_Data, FeatExtractedData
import os.path
import csv

def makejson(modelname,recordingID, vals):
    if modelname == "raw":
        data = SensorRawData.objects.filter(recording_id=recordingID).order_by('id')
    elif modelname == "proc":
        data = Preprocessed_Data.objects.filter(recording_id=recordingID).order_by('id')
    jsonstring = "{\"series\":["
    if hasattr(vals, '__iter__'):
        for valu in vals:
            jsonstring += "{\"data\": ["
            for record in data:
                jsonstring += record.store[valu] + ","
            jsonstring = jsonstring[:-1]
            jsonstring += "], \"name\": \""+valu+"\"},"
    else:
        jsonstring += "{\"data\": ["
        for record in data:
            jsonstring += record.store[vals] + ","
        jsonstring = jsonstring[:-1]
        jsonstring += "], \"name\": \""+vals+"\"},"
    jsonstring = jsonstring[:-1]
    jsonstring += "]}"
    return jsonstring

def getfeaturedata(recordingID):
    fpath = FeatExtractedData.objects.get(pp_recording=recordingID).path_to_file
    uncleanedfile = open(fpath,'r')
    if os.path.isfile(fpath+'p'):
        uncleanedfile.close()
    else:
        file = open(fpath+'p','w')
        for line in uncleanedfile:
            file.write(line.replace(' ',''))
        uncleanedfile.close()
        file.close()
    filecleaned = open(fpath+'p','r')
    #TODO replace the dictkey fucntion with a pull from the recoding database
    getkeys = csv.DictReader(filecleaned, delimiter=',')
    jsonstring = "{\"series\":["
    jsonstring += "{\"data\": ["
    csvreaderkeys = getkeys.next().keys()
    filecleaned.seek(0)
    csvreader = csv.DictReader(filecleaned, delimiter=',')
    valuesdictionary = {k: [] for k in csvreaderkeys}
    for line in csvreader:
        for ky in csvreaderkeys:
            valuesdictionary[ky].append(line[ky])
    for dictkeyname in valuesdictionary.keys():
        for valu in valuesdictionary[dictkeyname]:
            jsonstring += str(valu) + ","
        jsonstring = jsonstring[:-1]
        jsonstring += "], \"name\": \""+dictkeyname+"\"},"
    jsonstring = jsonstring[:-1]
    jsonstring += "]}"
    filecleaned.close()
    return jsonstring

def getavaliabledatavals(recordingID):
    keys = Recording.objects.get(id=recordingID).dict_keys
    return keys

# #MODIFYING OUTPUT FORMAT
#     mykey = [(i,i) for i in keys]