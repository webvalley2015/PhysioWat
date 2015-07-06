__author__ = 'andrew'

from PhysioWat.models import Recording,SensorRawData,Preprocessed_Data

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


def getavaliabledatavals(recordingID):
    keys = Recording.objects.get(id=recordingID).dict_keys
    return keys

# #MODIFYING OUTPUT FORMAT
#     mykey = [(i,i) for i in keys]