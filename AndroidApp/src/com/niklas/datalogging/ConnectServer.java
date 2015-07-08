package com.niklas.datalogging;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Calendar;
import java.util.TimeZone;

import com.unibo.cupidnodelogging.R;

import android.os.AsyncTask;
import android.os.CountDownTimer;
import android.os.Environment;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.RotateAnimation;
import android.widget.ImageView;
import android.widget.Toast;



public class ConnectServer extends AsyncTask<Void, String, Void> {

    @Override
    protected Void doInBackground(Void... params) {
    	
    	
    	String clientSentence = "Hello Internet";
    	
    	TimeZone tz = TimeZone.getTimeZone("Europe/Rome");
    	Calendar rightNow = Calendar.getInstance(tz);// .getInstance();

        Socket socket = null;
        DataOutputStream dataOutputStream = null;
        
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        
        String url = "192.168.210.183:5432";
       
        
        String ret = "";
        
        InputStream inputStream;
        
        

        try {
        	
        	if (MainActivity.isTheFileNew) {
        		File file = new File(Environment.getExternalStorageDirectory().getAbsolutePath()+"/CUPID_data/"+rightNow.get(Calendar.DAY_OF_MONTH)+"_"+ (rightNow.get(Calendar.MONTH) + 1) +"_"+ rightNow.get(Calendar.YEAR) +"/",
        		        MainActivity.file_name_log);
        	
            	inputStream = new FileInputStream(file);
        	}
            	
            else
            	inputStream = new FileInputStream(FileChooser.newFileChoosed);
           

            if ( inputStream != null ) {
                InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
                BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
                String receiveString = "";
                StringBuilder stringBuilder = new StringBuilder();

                while ( (receiveString = bufferedReader.readLine()) != null ) {
                    stringBuilder.append(receiveString);
                }

                inputStream.close();
                ret = stringBuilder.toString();
            }
        }
        catch (FileNotFoundException e) {
            Log.e("login activity", "File not found: " + e.toString());
        } catch (IOException e) {
            Log.e("login activity", "Can not read file: " + e.toString());
        }
        
        
        /*
        try {
        HttpClient httpclient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost(url);
        InputStreamEntity reqEntity = new InputStreamEntity(
        new FileInputStream(file), -1);
        reqEntity.setContentType("binary/octet-stream");
        reqEntity.setChunked(true); // Send in multiple parts if needed
        httppost.setEntity(reqEntity);
        //HttpResponse response = httpclient.execute(httppost);
        //Do something with response...
        }
         */
        

        try {
         //socket = new Socket("192.168.210.183", 5432);
         socket = new Socket();
         socket.connect(new InetSocketAddress("192.168.210.183", 5432), 3000);
         dataOutputStream = new DataOutputStream(socket.getOutputStream());
         dataOutputStream.writeBytes(ret);
         
         //dataOutputStream.writeUTF("Hello Internet" + "\n");
         
        } 
        
        catch (UnknownHostException e) {
         // TODO Auto-generated catch block
        	publishProgress("UnknownHostException");
         e.printStackTrace();
        } catch (IOException e) {
         // TODO Auto-generated catch block
        	publishProgress("Can't connect to server!");
         e.printStackTrace();
        }
        
        finally{
         if (socket != null){
          try {
           socket.close();
          } catch (IOException e) {
           // TODO Auto-generated catch block
        	  publishProgress("IOException: 2");
           e.printStackTrace();
          }
         }

         if (dataOutputStream != null){
          try {
           dataOutputStream.close();
          } catch (IOException e) {
           // TODO Auto-generated catch block
        	  publishProgress("IOException: 3");
           e.printStackTrace();
          }
         }
        }
        return null;
    }

    @Override
    protected void onProgressUpdate(String... values) {
    	writeLogMessage.writeLogMessage(values[0], true);
    }
    
    
}