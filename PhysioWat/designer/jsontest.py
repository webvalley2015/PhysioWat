__author__ = 'andrew'

import jsongen

def runtest():
    print jsongen.getavaliabledatavals(5)
    str = jsongen.makejson("raw","5",[" MagX","AccY","GyrZ"])
    print str
    f = open('acc.json','w')
    f.write(str)
    f.close()