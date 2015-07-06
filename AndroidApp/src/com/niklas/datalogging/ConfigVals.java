package com.niklas.datalogging;

import java.io.File;
import java.util.Calendar;
import java.util.TimeZone;

import android.os.Environment;

public class ConfigVals {
	
	private static File root = Environment.getExternalStorageDirectory();
	public static String gpsData_fn = 				"GPS_LogData.txt";
	public static String gpsData_klm_fn = 			"GPS_LogData.kml";
	public static final long plotInterval = 50; //Refresh time in ms
	
	public static final int EXELs3_NODE = 0;
	public static final int EXELs1_NODE = 1;
	public static final int GENERIC_NODE = 2;
	public static final int FLORIMAGE_NODE = 3;
	public static final int CEREBRO_NODE = 4;
	public static final String[] nodeTypeName = new String[] {"Exel s3", "Exel s1", "Generic", "Florimage", "Cerebro Node"};
	public static int nodeType = EXELs3_NODE;
	
	private static String start = "= =";
	private static String stop = ": :";
	public static char[] startStr = start.toCharArray(); 
	public static char[] stopStr = stop.toCharArray();
	
 	static TimeZone tz = TimeZone.getTimeZone("Europe/Rome");
	static Calendar rightNow = Calendar.getInstance(tz);// .getInstance();
	public static String folderName = root.getAbsolutePath()+	"/CUPID_data/"+rightNow.get(Calendar.DAY_OF_MONTH)+"_"+ (rightNow.get(Calendar.MONTH) + 1) +"_"+ rightNow.get(Calendar.YEAR) +"/";
	
	public static String getGPSfilename(){
		return "GPS_LogData_"+rightNow.get(Calendar.DAY_OF_YEAR)+"_"+rightNow.get(Calendar.HOUR_OF_DAY)+"."+rightNow.get(Calendar.MINUTE)+".txt";
	}
	public static String getKMLfilename(){
		return "GPS_LogData_"+rightNow.get(Calendar.DAY_OF_YEAR)+"_"+rightNow.get(Calendar.HOUR_OF_DAY)+"."+rightNow.get(Calendar.MINUTE)+".kml";
	}
	
}
