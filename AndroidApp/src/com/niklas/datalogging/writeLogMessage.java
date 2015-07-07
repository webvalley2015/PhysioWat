package com.niklas.datalogging;

import com.unibo.cupidnodelogging.R;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Vibrator;
import android.text.format.Time;
import android.widget.Toast;

public class writeLogMessage {
	
    private static final int NOTIFY_ME_ID=1337;

	public static void writeLogMessage(String message, boolean error) {
    	Time today = new Time(Time.getCurrentTimezone());
    	today.setToNow();
    	String logstring = today.format("%k:%M:%S") + "  ";
    	
    	if (error) {
    		logstring = logstring + "Error: ";
        final NotificationManager mgr=
                (NotificationManager)MainActivity.getAppContext().getSystemService(Context.NOTIFICATION_SERVICE);
            @SuppressWarnings("deprecation")
			Notification note=new Notification(R.drawable.stat_notify_chat,
                                                            "PhysioWAT",
                                                            System.currentTimeMillis());
             
            // This pending intent will open after notification click
            PendingIntent i=PendingIntent.getActivity(MainActivity.getAppContext(), 0,
                                                    new Intent(MainActivity.getAppContext(), NotificationOne.class),
                                                    0);
             
            note.setLatestEventInfo(MainActivity.getAppContext(), "PhysioWAT",
                                    "Error: "+ message, i);
             
            //After uncomment this line you will see number of notification arrived
            //note.number=2;
            mgr.notify(NOTIFY_ME_ID, note);
            
            Vibrator vibrator = (Vibrator)MainActivity.getAppContext().getSystemService(Context.VIBRATOR_SERVICE);
            vibrator.vibrate(2000);		
            
    	}
    	
    	logstring = logstring + message;
    	
    	MainActivity.listAdapter.add(logstring);
    	MainActivity.mainlogList1.smoothScrollToPosition(MainActivity.listAdapter.getCount() - 1);
    	
 
    }
	
	
}