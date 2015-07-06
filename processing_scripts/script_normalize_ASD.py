import sys

filenames=sys.argv
filenames=filenames[1:]

columns_in=["timeStamp","packetCounter", "AccX","AccY","AccZ", "GyrX","GyrY","GyrZ", "MagX","MagY","MagZ"]
columns_out=["TIME", "ACCX","ACCY","ACCZ", "GYRX","GYRY","GYRZ", "MAGX","MAGY","MAGZ", "LAB"]
