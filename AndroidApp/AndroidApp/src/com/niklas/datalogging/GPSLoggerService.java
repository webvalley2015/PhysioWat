package com.niklas.datalogging;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DateFormat;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.HashMap;
import java.util.TimeZone;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.location.LocationProvider;
import android.os.Binder;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;
import android.widget.Toast;

public class GPSLoggerService extends Service {

	public static final String DATABASE_NAME = "GPSLOGGERDB";
	public static final String POINTS_TABLE_NAME = "LOCATION_POINTS";
	public static final String TRIPS_TABLE_NAME = "TRIPS";
	public static boolean ServiceRunning = false;
	
	private final DecimalFormat sevenSigDigits = new DecimalFormat("0.#######");
	private final DateFormat timestampFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");

	private LocationManager lm;
	private LocationListener locationListener;
	private SQLiteDatabase db;
	
	private static long minTimeMillis = 2000;
	private static long minDistanceMeters = 5;
	private static float minAccuracyMeters = 25;
	
	private int lastStatus = 0;
	private static boolean showingDebugToast = false;
	
	private static final String tag = "GPSLoggerService";
	
	File file = new File(ConfigVals.folderName + "/"+ConfigVals.getKMLfilename());
	FileWriter sdWriter = null;

	/** Called when the activity is first created. */
	private void startLoggerService() {

		// ---use the LocationManager class to obtain GPS locations---
		lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);

		locationListener = new MyLocationListener();

		lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 
				minTimeMillis, 
				minDistanceMeters,
				locationListener);
		initDatabase();
	}
	
	private void initDatabase() {
		db = this.openOrCreateDatabase(DATABASE_NAME, SQLiteDatabase.OPEN_READWRITE, null);
		db.execSQL("CREATE TABLE IF NOT EXISTS " +
				POINTS_TABLE_NAME + " (GMTTIMESTAMP VARCHAR, LATITUDE REAL, LONGITUDE REAL," +
						"ALTITUDE REAL, ACCURACY REAL, SPEED REAL, BEARING REAL);");
		db.close();
		Log.i(tag, "Database opened ok");
	}

	private void shutdownLoggerService() {
		lm.removeUpdates(locationListener);
	}

	public class MyLocationListener implements LocationListener {
		
		public void onLocationChanged(Location loc) {
			if (loc != null) {
				boolean pointIsRecorded = false;
				try {
					if (loc.hasAccuracy() && loc.getAccuracy() <= minAccuracyMeters) {
						pointIsRecorded = true;
						GregorianCalendar greg = new GregorianCalendar();
						TimeZone tz = greg.getTimeZone();
						int offset = tz.getOffset(System.currentTimeMillis());
						greg.add(Calendar.SECOND, (offset/1000) * -1);
						StringBuffer queryBuf = new StringBuffer();
						queryBuf.append("INSERT INTO "+POINTS_TABLE_NAME+
								" (GMTTIMESTAMP,LATITUDE,LONGITUDE,ALTITUDE,ACCURACY,SPEED,BEARING) VALUES (" +
								"'"+timestampFormat.format(greg.getTime())+"',"+
								loc.getLatitude()+","+
								loc.getLongitude()+","+
								(loc.hasAltitude() ? loc.getAltitude() : "NULL")+","+
								(loc.hasAccuracy() ? loc.getAccuracy() : "NULL")+","+
								(loc.hasSpeed() ? loc.getSpeed() : "NULL")+","+
								(loc.hasBearing() ? loc.getBearing() : "NULL")+");");
						Log.i(tag, queryBuf.toString());
						db = openOrCreateDatabase(DATABASE_NAME, SQLiteDatabase.OPEN_READWRITE, null);
						db.execSQL(queryBuf.toString());
						String locData;
						locData =timestampFormat.format(greg.getTime())+ "\t"+loc.getLatitude()+"\t"+
								loc.getLongitude()+"\t"+
								(loc.hasAltitude() ? loc.getAltitude() : "NULL")+"\t"+
								(loc.hasAccuracy() ? loc.getAccuracy() : "NULL")+"\t"+
								(loc.hasSpeed() ? loc.getSpeed() : "NULL")+"\t"+
								(loc.hasBearing() ? loc.getBearing() : "NULL")+";\n";
						sdWriter.write(locData);
						
					} 
				} catch (Exception e) {
					Log.e(tag, e.toString());
				} finally {
					if (db.isOpen())
						db.close();
				}
				if (pointIsRecorded) {
					if (showingDebugToast) Toast.makeText(
							getBaseContext(),
							"Location stored: \nLat: " + sevenSigDigits.format(loc.getLatitude())
									+ " \nLon: " + sevenSigDigits.format(loc.getLongitude())
									+ " \nAlt: " + (loc.hasAltitude() ? loc.getAltitude()+"m":"?")
									+ " \nAcc: " + (loc.hasAccuracy() ? loc.getAccuracy()+"m":"?"),
							Toast.LENGTH_SHORT).show();
				} else {
					if (showingDebugToast) Toast.makeText(
							getBaseContext(),
							"Location not accurate enough: \nLat: " + sevenSigDigits.format(loc.getLatitude())
									+ " \nLon: " + sevenSigDigits.format(loc.getLongitude())
									+ " \nAlt: " + (loc.hasAltitude() ? loc.getAltitude()+"m":"?")
									+ " \nAcc: " + (loc.hasAccuracy() ? loc.getAccuracy()+"m":"?"),
							Toast.LENGTH_SHORT).show();
				}
			}
		}

		public void onProviderDisabled(String provider) {
			if (showingDebugToast) Toast.makeText(getBaseContext(), "onProviderDisabled: " + provider,
					Toast.LENGTH_SHORT).show();

		}

		public void onProviderEnabled(String provider) {
			if (showingDebugToast) Toast.makeText(getBaseContext(), "onProviderEnabled: " + provider,
					Toast.LENGTH_SHORT).show();

		}

		public void onStatusChanged(String provider, int status, Bundle extras) {
			String showStatus = null;
			if (status == LocationProvider.AVAILABLE)
				showStatus = "Available";
			if (status == LocationProvider.TEMPORARILY_UNAVAILABLE)
				showStatus = "Temporarily Unavailable";
			if (status == LocationProvider.OUT_OF_SERVICE)
				showStatus = "Out of Service";
			if (status != lastStatus && showingDebugToast) {
				Toast.makeText(getBaseContext(),
						"new status: " + showStatus,
						Toast.LENGTH_SHORT).show();
			}
			lastStatus = status;
		}

	}

	// Below is the service framework methods
	@Override
	public void onCreate() {
		super.onCreate();
		startLoggerService();
		ServiceRunning = true;
		try {
			sdWriter = new FileWriter(file, false);
			sdWriter.write("Timestamp \t Latitude \t Longitude \t Altitude \t Accuracy (m) \t Speed (m/s) \t Bearing (deg) \n");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}	
	}

	@Override
	public void onDestroy() {
		super.onDestroy();
		shutdownLoggerService();
		
		try {
			doExport();
			sdWriter.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}


	}


	// This is the object that receives interactions from clients. See
	// RemoteService for a more complete example.
	private final IBinder mBinder = new LocalBinder();

	@Override
	public IBinder onBind(Intent intent) {
		return mBinder;
	}

	public static void setMinTimeMillis(long _minTimeMillis) {
		minTimeMillis = _minTimeMillis;
	}

	public static long getMinTimeMillis() {
		return minTimeMillis;
	}

	public static void setMinDistanceMeters(long _minDistanceMeters) {
		minDistanceMeters = _minDistanceMeters;
	}

	public static long getMinDistanceMeters() {
		return minDistanceMeters;
	}

	public static float getMinAccuracyMeters() {
		return minAccuracyMeters;
	}
	
	public static void setMinAccuracyMeters(float minAccuracyMeters) {
		GPSLoggerService.minAccuracyMeters = minAccuracyMeters;
	}

	public static void setShowingDebugToast(boolean showingDebugToast) {
		GPSLoggerService.showingDebugToast = showingDebugToast;
	}

	public static boolean isShowingDebugToast() {
		return showingDebugToast;
	}

	/**
	 * Class for clients to access. Because we know this service always runs in
	 * the same process as its clients, we don't need to deal with IPC.
	 */
	public class LocalBinder extends Binder {
		GPSLoggerService getService() {
			return GPSLoggerService.this;
		}
	}

	
	private void doExport() {
		// export the db contents to a kml file
		SQLiteDatabase db = null;
		Cursor cursor = null;
		try {
			db = openOrCreateDatabase(GPSLoggerService.DATABASE_NAME, SQLiteDatabase.OPEN_READWRITE, null);
			cursor = db.rawQuery("SELECT * " +
                    " FROM " + GPSLoggerService.POINTS_TABLE_NAME +
                    " ORDER BY GMTTIMESTAMP ASC",
                    null);
            int gmtTimestampColumnIndex = cursor.getColumnIndexOrThrow("GMTTIMESTAMP");
            int latitudeColumnIndex = cursor.getColumnIndexOrThrow("LATITUDE");
            int longitudeColumnIndex = cursor.getColumnIndexOrThrow("LONGITUDE");
            int altitudeColumnIndex = cursor.getColumnIndexOrThrow("ALTITUDE");
            int accuracyColumnIndex = cursor.getColumnIndexOrThrow("ACCURACY");
			if (cursor.moveToFirst()) {
				StringBuffer fileBuf = new StringBuffer();
				StringBuffer coordBuffer = new StringBuffer();
				String beginTimestamp = null;
				String endTimestamp = null;
				String gmtTimestamp = null;
				initFileBuf(fileBuf, initValuesMap());
				do {
					gmtTimestamp = cursor.getString(gmtTimestampColumnIndex);
					if (beginTimestamp == null) {
						beginTimestamp = gmtTimestamp;
					}
					double latitude = cursor.getDouble(latitudeColumnIndex);
					double longitude = cursor.getDouble(longitudeColumnIndex);
					double altitude = cursor.getDouble(altitudeColumnIndex);
					double accuracy = cursor.getDouble(accuracyColumnIndex);
					addPointToBuff(fileBuf,gmtTimestamp,latitude,longitude, altitude);
					coordBuffer.append(sevenSigDigits.format(longitude)+","+sevenSigDigits.format(latitude)+","+altitude+"\n");
				} while (cursor.moveToNext());
				endTimestamp = gmtTimestamp;
				
				addPathToBuf(fileBuf,coordBuffer,initValuesMap());
				closeFileBuf(fileBuf, beginTimestamp, endTimestamp);
				String fileContents = fileBuf.toString();
				
				//Log.d(tag, fileContents);
				File fileKLM = new File(ConfigVals.folderName + "/"+ConfigVals.getKMLfilename());
				FileWriter sdWriterKLM = new FileWriter(fileKLM, false);
				sdWriterKLM.write(fileContents);
				sdWriterKLM.close();
    			Toast.makeText(getBaseContext(),
    					"Export completed!",
    					Toast.LENGTH_LONG).show();
			} else {
				Log.i("Gps logger","I didn't find any GPS location point, so no KML file was exported.");
//				Toast.makeText(getBaseContext(),
//						"I didn't find any location points in the database, so no KML file was exported.",
//						Toast.LENGTH_SHORT).show();
			}
		} catch (FileNotFoundException fnfe) {
			Toast.makeText(getBaseContext(),
					"Error trying access the SD card.  Make sure your handset is not connected to a computer and the SD card is properly installed",
					Toast.LENGTH_LONG).show();
		} catch (Exception e) {
			Toast.makeText(getBaseContext(),
					"Error trying to export: " + e.getMessage(),
					Toast.LENGTH_LONG).show();
		} finally {
			if (cursor != null && !cursor.isClosed()) {
				cursor.close();
			}
			if (db != null && db.isOpen()) {
				db.execSQL("DELETE FROM "+GPSLoggerService.POINTS_TABLE_NAME);
				db.close();
			}
		}
	}
	
	private void addPointToBuff(StringBuffer fileBuf,String timestamp, double latitude,
			double longitude, double altitude) {
		fileBuf.append("        <Placemark>\n");
		fileBuf.append("           <TimeStamp>\n");
		fileBuf.append("              <when>"+timestamp+"</when>\n");
		fileBuf.append("           </TimeStamp>\n");
		fileBuf.append("           <styleUrl>#dot-icon</styleUrl>\n");
		fileBuf.append("           <Point>\n");
		fileBuf.append("              <coordinates>"+sevenSigDigits.format(longitude)+","+sevenSigDigits.format(latitude)+","+sevenSigDigits.format(altitude)+"</coordinates>\n");
		fileBuf.append("           </Point>\n");	
		fileBuf.append("        </Placemark>\n");
	}

	private HashMap<String, String> initValuesMap() {
		HashMap<String, String> valuesMap = new HashMap<String, String>();
		valuesMap.put("FILENAME", ConfigVals.getKMLfilename());
		
		// use ground settings for the export
		valuesMap.put("EXTRUDE", "0");
		valuesMap.put("TESSELLATE", "1");
		valuesMap.put("ALTITUDEMODE", "clampToGround");

		return valuesMap;
	}
	
	private void closeFileBuf(StringBuffer fileBuf, String beginTimestamp, String endTimestamp) {
		fileBuf.append("        </coordinates>\n");
		fileBuf.append("     </LineString>\n");
//		fileBuf.append("	 <TimeSpan>\n");
//		String formattedBeginTimestamp = zuluFormat(beginTimestamp);
//		fileBuf.append("		<begin>"+formattedBeginTimestamp+"</begin>\n");
//		String formattedEndTimestamp = zuluFormat(endTimestamp);
//		fileBuf.append("		<end>"+formattedEndTimestamp+"</end>\n");
//		fileBuf.append("	 </TimeSpan>\n");
		fileBuf.append("    </Placemark>\n");
		fileBuf.append("  </Document>\n");
		fileBuf.append("</kml>");
	}
	
	private String zuluFormat(String beginTimestamp) {
		// turn 20081215135500 into 2008-12-15T13:55:00Z
		StringBuffer buf = new StringBuffer(beginTimestamp);
		buf.insert(4, '-');
		buf.insert(7, '-');
		buf.insert(10, 'T');
		buf.insert(13, ':');
		buf.insert(16, ':');
		buf.append('Z');
		return buf.toString();
	}


	private void initFileBuf(StringBuffer fileBuf, HashMap<String, String> valuesMap) {
		fileBuf.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
		fileBuf.append("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n");
		fileBuf.append("  <Document>\n");
		fileBuf.append("    <name>"+valuesMap.get("FILENAME")+"</name>\n");
		fileBuf.append("    <description>GPSLogger KML export</description>\n");
		fileBuf.append("    <Style id=\"dot-icon\">\n");
		fileBuf.append("       <IconStyle>\n");
		fileBuf.append("          <Icon>\n");
		fileBuf.append("             <href>http://maps.google.com/intl/en_us/mapfiles/ms/micons/green.png</href>\n");
		fileBuf.append("          </Icon>\n");
		fileBuf.append("       </IconStyle>\n");
		fileBuf.append("    </Style>\n");
	}
		
		
		
		
		
	private void addPathToBuf(StringBuffer fileBuf,StringBuffer coord, HashMap<String, String> valuesMap) {	
		fileBuf.append("   <Placemark>\n");
		fileBuf.append("    <Style id=\"RedLine\">\n");
		fileBuf.append("      <LineStyle>\n");
		fileBuf.append("        <color>ff0000ff</color>\n");
		fileBuf.append("        <width>3</width>\n");
		fileBuf.append("      </LineStyle>\n");
		fileBuf.append("    </Style>\n");
//		fileBuf.append("    <Placemark>\n");
		fileBuf.append("      <name>Patient's path</name>\n");
		fileBuf.append("      <description>patient's path dring gait rehabilitation training</description>\n");
//		fileBuf.append("      <styleUrl>#yellowLineGreenPoly</styleUrl>\n");
		fileBuf.append("      <LineString>\n");
		fileBuf.append("        <extrude>"+valuesMap.get("EXTRUDE")+"</extrude>\n");
		fileBuf.append("        <tessellate>"+valuesMap.get("TESSELLATE")+"</tessellate>\n");
		fileBuf.append("        <altitudeMode>"+valuesMap.get("ALTITUDEMODE")+"</altitudeMode>\n");
		fileBuf.append("        <coordinates>\n");
		fileBuf.append(coord+"\n");
	}
	
}
