package com.niklas.datalogging;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.List;
import java.util.TimeZone;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import com.niklas.datalogging.BluetoothChatService;
import com.niklas.datalogging.DeviceListActivity;
import com.niklas.datalogging.SettingsActivity;
import com.unibo.cupidnodelogging.R;

import android.app.Activity;
import android.app.ActionBar;
import android.app.Fragment;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.res.Configuration;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.os.Debug;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.text.format.Time;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.view.View.OnClickListener;
import android.view.animation.Animation;
import android.view.animation.RotateAnimation;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import com.androidplot.util.Redrawer;

public class MainActivity extends Activity implements
		ActionBar.OnNavigationListener {

	/**
	 * The serialization (saved instance state) Bundle key representing the
	 * current dropdown position.
	 */
	private static final String STATE_SELECTED_NAVIGATION_ITEM = "selected_navigation_item";
	  private static final String TAG = "BluetoothChat";
	    private static final boolean D = true;
	    
	    static boolean serverProtocolState;

	    // Message types sent from the BluetoothChatService Handler
	    public static final int MESSAGE_STATE_CHANGE = 1;
	    public static final int MESSAGE_READ = 2;
	    public static final int MESSAGE_WRITE = 3;
	    public static final int MESSAGE_DEVICE_NAME = 4;
	    public static final int MESSAGE_TOAST = 5;

	    // Key names received from the BluetoothChatService Handler
	    public static final String DEVICE_NAME = "device_name";
	    public static final String TOAST = "toast";
	    public static final String SENS_DATA = "sensorData";
	    
	    // Intent request codes
	    private static final int REQUEST_CONNECT_DEVICE_INSECURE = 2;
	    private static final int REQUEST_ENABLE_BT = 3;
	    private static final int REQUEST_SUBMIT_SETTINGS = 4;
	   

	    // Layout Views
	    private Button mSendStartWalkButton;
	    private Button mSendStartRunButton;

	    private Button mSendStopButton;
	    public int ConnectedDevices;

	    // Name of the connected device
	    private String mConnectedDeviceName = null;

	    private BluetoothAdapter mBluetoothAdapter = null;
	    public static final int MaxNodes = 7;
	    // Member object for the chat services
	    private static BluetoothChatService[] mChatService = new BluetoothChatService[MaxNodes];
	    
	    //private String[] ConnectedDevicesNames = new String[MaxNodes];
	    
	    public String dirName, dirName2,update_name_log,file_name_log;
	    File root;
	    //private int day, month, year,l_num;
	    private File log_file;
	    private FileWriter log_file_wr;
	    private BufferedWriter out_log;
	    private int[] stringCnt = new int[7];
//	    private ConnectionManager mConnManager = new ConnectionManager();

	    private Redrawer redrawer;
	    
	    private UI_Management mUImang = null;
	    
	    public final static String keyBundle = "SettingsBundleKey";
	    
	    //private static int ConnectedDevices = 0;
	    private Time now = new Time(); 
	    private final Handler[] mHandler = new Handler[MaxNodes];

	    
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
        if(D) Log.e(TAG, "+++ ON CREATE +++");

        // Get local Bluetooth adapter
        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
  
        // If the adapter is null, then Bluetooth is not supported
        if (mBluetoothAdapter == null) {
            Toast.makeText(this, "Bluetooth is not available", Toast.LENGTH_LONG).show();
            finish();
            return;
        }
        
//        for (int i = 0; i < MaxNodes; i++) {
//        	ConnectedDevicesNames[i] = "";
//        }
        Arrays.fill(stringCnt, (byte) 0);

        
		// Set up the action bar to show a dropdown list.
		final ActionBar actionBar = getActionBar();
		
		actionBar.setDisplayShowTitleEnabled(false);
		actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_LIST);

		// Set up the dropdown list navigation in the action bar.
		actionBar.setListNavigationCallbacks(
		// Specify a SpinnerAdapter to populate the dropdown list.
				new ArrayAdapter<String>(actionBar.getThemedContext(),
						android.R.layout.simple_list_item_1,
						android.R.id.text1, new String[] {
								getString(R.string.title_section1),
								getString(R.string.title_section2),
								getString(R.string.title_section3),
								getString(R.string.title_section4),}), this);
		
		setupHandler();
		
        // If BT is not on, request that it be enabled.
        // setupChat() will then be called during onActivityResult
        if (!mBluetoothAdapter.isEnabled()) {
            Intent enableIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableIntent, REQUEST_ENABLE_BT);
        // Otherwise, setup the chat session
        } else {
            if (mChatService[0] == null) 
            	setupChat();
        }
		ConnectionManager.init(this.getApplicationContext(),mChatService);
        
	}
	
    @Override
    public void onPause() {
        redrawer.pause();
        super.onPause();
        Log.e(TAG, "+++ ON PAUSE +++");
    }


    
    
    @Override
    public void onDestroy() {
        super.onDestroy();
        ConnectionManager.closeAll();
        redrawer.finish();
        mChatService = new BluetoothChatService[MaxNodes];
        Log.e(TAG, "+++ ON Destroy +++");
    }
	
    public void onStop() {
        super.onDestroy();        
        redrawer.finish();
//        ConnectionManager.closeAll();
        mUImang.deInitGraph();
        mUImang = null;

//        Debug.stopMethodTracing();
        Log.e(TAG, "+++ ON STOP +++");
    }
  
	 public void onStart() {
	        super.onStart();

	        this.getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);
	        if(D) 
	        	Log.e(TAG, "++ ON START ++");

//	        // If BT is not on, request that it be enabled.
//	        // setupChat() will then be called during onActivityResult
//	        if (!mBluetoothAdapter.isEnabled()) {
//	            Intent enableIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
//	            startActivityForResult(enableIntent, REQUEST_ENABLE_BT);
//	        // Otherwise, setup the chat session
//	        } else {
//	            if (mChatService[0] == null) 
//	            	setupChat();
//	        }
//			ConnectionManager.init(this.getApplicationContext(),mChatService);
			
			
			mUImang = new UI_Management(this,mChatService);
			redrawer = mUImang.initGraph();
			mUImang.initBtButtons();
//			redrawer.start();
			
	    }

	    @Override public void onResume(){
	    	super.onResume();
	    	
//	    	Debug.startMethodTracing("calc");

	    	 Log.e(TAG, "+++ ON RESUME +++");
	    }
	 
	@Override
	public void onRestoreInstanceState(Bundle savedInstanceState) {
		// Restore the previously serialized current dropdown position.
		if (savedInstanceState.containsKey(STATE_SELECTED_NAVIGATION_ITEM)) {
			getActionBar().setSelectedNavigationItem(
					savedInstanceState.getInt(STATE_SELECTED_NAVIGATION_ITEM));
		}
	}

	@Override
	public void onSaveInstanceState(Bundle outState) {
		// Serialize the current dropdown position.
		outState.putInt(STATE_SELECTED_NAVIGATION_ITEM, getActionBar()
				.getSelectedNavigationIndex());
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {

		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		Intent serverIntent = null;
		int id = item.getItemId();
		if (id == R.id.action_settings) {
        	Intent settingsIntent = new Intent(this, SettingsActivity.class);
//        	Bundle mBundle = new Bundle();
//        	mBundle.putString(keyBundle, "test");
//        	settingsIntent.putExtras(mBundle);
        	startActivityForResult(settingsIntent,REQUEST_SUBMIT_SETTINGS);
			return true;
		}
		if (id == R.id.action_connect){
            serverIntent = new Intent(this, DeviceListActivity.class);
            startActivityForResult(serverIntent, REQUEST_CONNECT_DEVICE_INSECURE);
            
		}
		if (id ==R.id.action_save_devices)
			ConnectionManager.saveDevices();
		
		return super.onOptionsItemSelected(item);
	}

	@Override
	public boolean onNavigationItemSelected(int position, long id) {
		// When the given dropdown item is selected, show its contents in the
		// container view.
		Log.i("navigationItem","Id Selected: "+ position);
		switch (position) {
		case 0:
			
		break;
		case 1:
			ConnectionManager.clearSavedDevices();
		break;
		case 2:
			ConnectionManager.closeAll();
		break;
		case 3:
			ConnectionManager.restoreBTDevices();
		break;
		
		}
		
		getFragmentManager()
				.beginTransaction()
				.replace(R.id.container,
						PlaceholderFragment.newInstance(position + 1)).commit();
		return true;
	}


	/**
	 * A placeholder fragment containing a simple view.
	 */
	public static class PlaceholderFragment extends Fragment {
		/**
		 * The fragment argument representing the section number for this
		 * fragment.
		 */
		private static final String ARG_SECTION_NUMBER = "section_number";

		/**
		 * Returns a new instance of this fragment for the given section number.
		 */
		public static PlaceholderFragment newInstance(int sectionNumber) {
			PlaceholderFragment fragment = new PlaceholderFragment();
			Bundle args = new Bundle();
			args.putInt(ARG_SECTION_NUMBER, sectionNumber);
			fragment.setArguments(args);
			
			
			return fragment;
		}

		public PlaceholderFragment() {
		}

		@Override
		public View onCreateView(LayoutInflater inflater, ViewGroup container,
				Bundle savedInstanceState) {
			View rootView = inflater.inflate(R.layout.fragment_main, container,
					false);
			return rootView;
		}
	}
	
    private void setupChat() {
        Log.d(TAG, "setupChat()");

        // Initialize the array adapter for the conversation thread
        
        mSendStartWalkButton = (Button) findViewById(R.id.buttonStartWalk);
        mSendStartWalkButton.setOnClickListener(new OnClickListener() {
            public void onClick(View v) {
                // Send a message using content of the edit text widget
                //TextView view = (TextView) findViewById(R.id.edit_text_out);
            	for (int i = 0; i< MaxNodes; i++){
            		if (mChatService[i].IsConnected)
            			get_log_num(mChatService[i].deviceName, 1, i,"Walk");
            	}
            	now.setToNow();
//            	mConversationArrayAdapter.add(now.format(TimeFormat) + "Walking Activity Started");
                String message = new String(ConfigVals.startStr);
                sendMessage(message);
                redrawer.start();
        		getApplicationContext().startService(new Intent(getApplicationContext(),
        				com.niklas.datalogging.GPSLoggerService.class));
        		if(getResources().getConfiguration().orientation == Configuration.ORIENTATION_PORTRAIT) {
        		    setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        		} else setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
        		
            }
        });
        
        
        
        mSendStartRunButton= (Button) findViewById(R.id.buttonStartRun);
        mSendStartRunButton.setOnClickListener(new OnClickListener() {
            public void onClick(View v) {
                // Send a message using content of the edit text widget
                //TextView view = (TextView) findViewById(R.id.edit_text_out);
            	for (int i = 0; i< MaxNodes; i++){
            		if (mChatService[i].IsConnected)
            			get_log_num(mChatService[i].deviceName, 1, i,"Run");
            	}
            	now.setToNow();
//            	mConversationArrayAdapter.add(now.format(TimeFormat) + "Running Activity Started");
                String message = new String(ConfigVals.startStr);
                sendMessage(message);
                redrawer.start();
                if(getResources().getConfiguration().orientation == Configuration.ORIENTATION_PORTRAIT) {
        		    setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        		} else setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
            }
        });
        

        
        mSendStopButton = (Button) findViewById(R.id.buttonSendStop);
        mSendStopButton.setOnClickListener(new OnClickListener() {
            public void onClick(View v) {
            	now.setToNow();
                String message = new String(ConfigVals.stopStr);
                sendMessage(message);
                redrawer.pause();
        		getApplicationContext().stopService(new Intent(getApplicationContext(),
        				com.niklas.datalogging.GPSLoggerService.class));
        		setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED);
            }
        });
        
        //+++++++++++++++++++++++++++Sending data to Server++++++++++++++++++++++++++++++++++
        
        mSendStopButton = (Button) findViewById(R.id.buttonSendToServer);
        mSendStopButton.setOnClickListener(new OnClickListener() {
            public void onClick(View v) {
            	final Context context = getApplicationContext();
            	CharSequence text;
            	int duration = Toast.LENGTH_SHORT;

            	if (serverProtocolState)
            		text = "Try to connect to Server...";
            	
            	else
            		text = "Please capture Data first";
            		
            	Toast toast = Toast.makeText(context, text, duration);
            	toast.show();
            	
            	if (serverProtocolState) {
            		final ImageView favicon = (ImageView) findViewById(R.id.imageView1);
            		favicon.setVisibility(View.VISIBLE);

            		RotateAnimation r; // = new RotateAnimation(ROTATE_FROM, ROTATE_TO);
            		r = new RotateAnimation(0, 720, Animation.RELATIVE_TO_SELF, 0.5f, Animation.RELATIVE_TO_SELF, 0.5f);
            		r.setDuration((long) 2*1500);
            		r.setRepeatCount(0);
            		favicon.startAnimation(r);
    	      
            		new CountDownTimer(3000, 100) {

            			public void onTick(long millisUntilFinished) {
            				// implement whatever you want for every tick
            			}

            			public void onFinish() {
            				favicon.setVisibility(View.GONE);
                    		
                        	Toast toast = Toast.makeText(context, "Success!", Toast.LENGTH_SHORT);
                        	toast.show();
            			}
            		}.start();
            		
            	}
                   	
            	PushToServer.pushFileToServer();
            }
        });
        
        //+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        // Initialize the BluetoothChatService to perform bluetooth connections
        for(int i = 0; i<7 ; i++){
        	mChatService[i] = new BluetoothChatService(this, mHandler[i]);
        }
    }
    
	
	private static int nodeIndex = 0;
	private static int getNodeIndex(){
		return nodeIndex;
	}
	
    private  final void setupHandler(){
    	for(int ind = 0; ind<7 ; ind++){
    	nodeIndex = ind;
			mHandler[ind] = new Handler() {
				public final int HandlerIndex = MainActivity.getNodeIndex();
				@Override
	            public void handleMessage(Message msg) {
					if (mUImang != null){
		                switch (msg.what) {
		                case MESSAGE_STATE_CHANGE:
		                    if(D) Log.i(TAG, "MESSAGE_STATE_CHANGE: " + msg.arg1);
		                    switch (msg.arg1) {
		                    case BluetoothChatService.STATE_CONNECTED:
		                    	mUImang.checkNodeStatus(mChatService);
		                    	mUImang.checkNames();
		                        break;
		                    case BluetoothChatService.STATE_DISCONNECTED:
		                    	mUImang.checkNodeStatus(mChatService);
		                    	break;
		                    case BluetoothChatService.STATE_CONNECTING:
		                    	mUImang.checkNodeStatus(mChatService);
		                        break;
		                    case BluetoothChatService.STATE_LISTEN:
		                    	mUImang.checkNodeStatus(mChatService);
		                    	break;
		                    case BluetoothChatService.STATE_NONE:
		                    	if (mUImang != null)
		                    		mUImang.checkNodeStatus(mChatService);	                    	
		                        break;
		                    }
		                    break;
		                case MESSAGE_WRITE:
		                    break;
		                case MESSAGE_READ:
		                	float[] data = new float[10];
		                	data = msg.getData().getFloatArray(SENS_DATA);
		                	mUImang.checkDataRead(HandlerIndex, data);
		                	
		                    break;
		                case MESSAGE_DEVICE_NAME:
		                    // save the connected device's name
		                    mConnectedDeviceName = msg.getData().getString(DEVICE_NAME);
		                    Toast.makeText(getApplicationContext(), "Connected to "
		                                   + mConnectedDeviceName, Toast.LENGTH_SHORT).show();
		                    
		                    break;
		                case MESSAGE_TOAST:
		                    Toast.makeText(getApplicationContext(), msg.getData().getString(TOAST),
		                                   Toast.LENGTH_SHORT).show();
		                    break;
		                }
		            }
				}
	        };
    	}
    	
    }
    
    
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if(D) Log.d(TAG, "onActivityResult " + resultCode);
        if (resultCode != 0){
	        switch (requestCode) {
	        case REQUEST_CONNECT_DEVICE_INSECURE:
	            // When DeviceListActivity returns with a device to connect
	        	int currState;
	        	String address = data.getExtras()
	                    .getString(DeviceListActivity.EXTRA_DEVICE_ADDRESS);
	                // Get the BLuetoothDevice object
	            BluetoothDevice device = mBluetoothAdapter.getRemoteDevice(address);
	        	for (int i=0; i<7; i++){
	        		currState = mChatService[i].getState();
	        		if (currState != BluetoothChatService.STATE_CONNECTED && 
	        				currState != BluetoothChatService.STATE_CONNECTING){
	        			mChatService[i].connect(device, false);
	        			return;
	        		}
	        	}
	
	        case REQUEST_ENABLE_BT:
	            // When the request to enable Bluetooth returns
	            if (resultCode == Activity.RESULT_OK) {
	                // Bluetooth is now enabled, so set up a chat session
	                setupChat();
	            } else {
	                // User did not enable Bluetooth or an error occured
	                Log.d(TAG, "BT not enabled");
	                Toast.makeText(this, R.string.bt_not_enabled_leaving, Toast.LENGTH_SHORT).show();
	                finish();
	            }
	            
	        case REQUEST_SUBMIT_SETTINGS:
	        	ArrayList<String> configStrings = data.getStringArrayListExtra("result");
	        	for (String conf : configStrings ){
	        		sendMessage(conf);
	        		char confStr[] = conf.toCharArray();
	        		
	        		try {
						Thread.sleep(500);
					} catch (InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
	        		
	        	}
	        	
	        	//Toast.makeText(this, configStrings.get(1), Toast.LENGTH_SHORT).show();
	        	break;
	        }
        }
    }
    
    
    /**
     * Sends a message.
     * @param message  A string of text to send.
     */
    private void sendMessage(String message) {
        // Check that there's actually something to send
        if (message.length() > 0) {
            // Get the message bytes and tell the BluetoothChatService to write
        	serverProtocolState = true;
        	int currState;
            byte[] send = message.getBytes();
            for (int i = 0; i < 7; i++){
            	currState = mChatService[i].getState();
        		if (currState ==  BluetoothChatService.STATE_CONNECTED){
        			mChatService[i].StartStremingTime = android.os.SystemClock.elapsedRealtime();
        			mChatService[i].write(send);
        		}
            }
            if (getnConnectedNodes() == 0){
                // Check that we're actually connected to any node
            	serverProtocolState = false;
                Toast.makeText(this, R.string.not_connected, Toast.LENGTH_SHORT).show();
                return;
            }
        }
    }
    

public int get_log_num(String node_id, int l_num_update,int service_id, String activity){
		
		if (mChatService[service_id].getState() == BluetoothChatService.STATE_CONNECTED){
	    	root = Environment.getExternalStorageDirectory();
		 	TimeZone tz = TimeZone.getTimeZone("Europe/Rome");
	
			Calendar rightNow = Calendar.getInstance(tz);// .getInstance();
			dirName=ConfigVals.folderName;
			//dirName2="CUPID_data/"+rightNow.get(Calendar.DAY_OF_MONTH)+"_"+ (rightNow.get(Calendar.MONTH) + 1) +"_"+ rightNow.get(Calendar.YEAR) +"/";
	    	
			try{
//	    		    dirName = "/sdcard/"+dirName2;
//	    			//dirName = Environment.getExternalStorageDirectory().getPath()+dirName2;
	    		    File newFile = new File(dirName);
	    		    newFile.mkdirs();
	
	    	} 
	    	catch(Exception e)
	    	{
	    		Toast.makeText(this, "Exception creating folder " + e, Toast.LENGTH_LONG).show();
	    	} 
	    	
			if (root.canRead()) {
	
			}
			if (root.canWrite()){
				
				file_name_log = "log_"+rightNow.get(Calendar.DAY_OF_YEAR)+"_"+rightNow.get(Calendar.HOUR_OF_DAY)+"."+rightNow.get(Calendar.MINUTE)+"."+rightNow.get(Calendar.SECOND)+"_"+"_"+node_id+".txt";	
				
				//log_file = new File(root,"log_data/"+file_name_log);
				log_file = new File(dirName,file_name_log);
				
				
				try {
					log_file_wr = new FileWriter(log_file);
					out_log = new BufferedWriter(log_file_wr);
					
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
					mChatService[service_id].setOutFile(out_log);
			}
		}
	
	    	return 1;
	 }

	public static int getnConnectedNodes(){
		int nNodes = 0;
		for (int i = 0; i<MaxNodes; i++){
			if (mChatService[i] != null){
				if(mChatService[i].IsConnected)
					nNodes++;
			}
		}
	
		return nNodes;
}
    
}
