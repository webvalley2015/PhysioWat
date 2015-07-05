__author__ = 'andrew'

from PhysioWat.models import Recording,SensorRawData,PreprocessedData


def makejson(modelname,recordingID, vals):
    if modelname == "raw":
        data = SensorRawData.objects.filter(recording_id=recordingID)
    elif modelname == "proc":
        data = PreprocessedData.objects.filter(recording_id=recordingID)
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
