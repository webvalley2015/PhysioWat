package com.niklas.datalogging;

import java.io.File;
import java.io.FileInputStream;
import java.util.Calendar;
import java.util.TimeZone;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.InputStreamEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import android.os.Environment;


public class PushToServer {
 	static TimeZone tz = TimeZone.getTimeZone("Europe/Rome");
	static Calendar rightNow = Calendar.getInstance(tz);// .getInstance();
	
	public static void pushFileToServer(){
		String url = "192.168.210.183:5432";
		File file = new File(Environment.getExternalStorageDirectory().getAbsolutePath()+"/CUPID_data/"+rightNow.get(Calendar.DAY_OF_MONTH)+"_"+ (rightNow.get(Calendar.MONTH) + 1) +"_"+ rightNow.get(Calendar.YEAR) +"/",
		        "log_183_9.36.38__EXLs3_0175.txt");
		try {
		    HttpClient httpclient = new DefaultHttpClient();

		    HttpPost httppost = new HttpPost(url);

		    InputStreamEntity reqEntity = new InputStreamEntity(
		            new FileInputStream(file), -1);
		    reqEntity.setContentType("binary/octet-stream");
		    reqEntity.setChunked(true); // Send in multiple parts if needed
		    httppost.setEntity(reqEntity);
		    HttpResponse response = httpclient.execute(httppost);
		    //Do something with response...

		} catch (Exception e) {
		    // show error
		}
	}

}
