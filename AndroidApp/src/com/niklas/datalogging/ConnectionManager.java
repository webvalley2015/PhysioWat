package com.niklas.datalogging;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;

import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.os.SystemClock;
import android.util.Log;
import android.widget.Toast;


/** 
 * Topmost routine for setting and checking connections (all of them: this is not node-specific). </br>
 * Static members of this class contain imuExtractor object, eventually obtained through connection routine.</br>
 * High level methods are also provided to manage connection status.
 */
public class ConnectionManager {
	public static Context mContext;
	public static Handler guiHandler;
	private static BluetoothChatService[] BTservice = new BluetoothChatService[MainActivity.MaxNodes];
//	public static NodesHandler[] mNodesHandler;
//	public static ImuExtractor[] imuExtractor;
//	public static File[] rawSamplesSrc;
//	public static ArrayList<Integer> savedNodesInd = new ArrayList<Integer>(); 
	
	private BluetoothAdapter mBluetoothAdapter = null;
	
//	private final int connectionTTL = 7000;
	
//	private static int[] BattVals = new int[3];
	private final String logTag = "ConnManager";
	
    // Intent request codes
	
	private boolean irq = false;
	
	/**
	 * Allow to set Context and Handlers for this routine, so that it can communicate with actual activity's GUI
	 * @param c current Context
	 * @param h a generic handler created in GUI's thread 
	 * @param nh an array (one per node) of specialized handlers (NodesHandler) for nodes-to-gui communications
	 * @see NodesHandler
	 */
	public static void init(Context c,BluetoothChatService[] serviceLink) {
		ConnectionManager.mContext = c;
		for (int i=0; i<MainActivity.MaxNodes; i++)
		BTservice[i] = serviceLink[i];
//		ConnectionManager.guiHandler =h;  
//		ConnectionManager.mNodesHandler = nh;
//		BattVals = new int[] {100, 100, 100};
		
//		if (imuExtractor == null)
//			imuExtractor = new ImuExtractor[CfgData.nodesMax];
//		
//		for (int i = 0; i < imuExtractor.length; i++) 
//			if (imuExtractor[i] != null)  
//				imuExtractor[i].setHandler(nh[i]);
			
		restoreDevices();
		
//		for (ImuExtractor ie :  imuExtractor) 
//			if (ie != null)  
//				ie.refreshHandler();
		
		
	}
	
	
	public void interrupt() {
		irq= true;
	}
	
//	@Override
//	public void run() {
//		irq = false;
//		
//		Log.i("ConnManager", "* Beginning connection routine *");
//		
//		if (isAllConnected()) {
////			FSM.handle(FSM.Message.END_OF_ROUTINE); 
//			return;
//		}
//
////		if(CfgData.simulMode) {
////			restoreFileDevices();
////			
////		}  else { 
//			mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
//			
//	    	// If BT is not on, request that it be enabled.
//	    	if (!mBluetoothAdapter.isEnabled()) {
//	    		Intent enableIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
////	    		((Activity) mContext).startActivityForResult(enableIntent, AdminActivity.REQUEST_ENABLE_BT); 
//	    		((Activity) mContext).startActivity(enableIntent); 
////	    		FSM.handle(FSM.Message.END_OF_ROUTINE);
////	    		FSM.handle(FSM.Message.CHECK_CONNECTION);
//	    		return;
////	    	}  else if (!restoreBTDevices()){
////				guiHandler.post(new Runnable(){ public void run() {
////					Toast.makeText(mContext, R.string.toast_no_device_file_found, Toast.LENGTH_SHORT).show();
////				}});
////				FSM.handle(FSM.Message.END_OF_ROUTINE);
//////				FSM.handle(FSM.Message.CHECK_CONNECTION);
////				return;
////	    	}
////			} else connectAll();
//		}
//		
//		connectAll();
//		
//		long connInitTime = SystemClock.elapsedRealtime();
////		while (isConnecting() && !irq && (SystemClock.elapsedRealtime()-connInitTime) < connectionTTL) 
////		while (isConnecting() && !irq) 
////			try {Thread.sleep(5);} catch (InterruptedException e) {}
//		
//
//		/* notify connection routine results */
//		if (!irq) {
//			if (isConnected()) {
//				try {Thread.sleep(5);} catch (InterruptedException e) {}
//				Log.i(logTag,"Connection was succesfully set");
////				for (int i = 0; i < CfgData.nodesMax; i++) 
////					if (imuExtractor[i] != null)
////						imuExtractor[i].initNode();
//			} else {
//				try {Thread.sleep(5);} catch (InterruptedException e) {}
//				Log.i(logTag,"Connection failed.");
////				if (mNodesHandler[0] != null) {
////					mNodesHandler[0].post(new Runnable(){ public void run() {
//						Toast.makeText(mContext, "Connection failed. Check sensors status and try again!", Toast.LENGTH_SHORT).show();
////					}});
////				}
//			}
//		} 
////		else if (irq) {
////			for (int i = 0; i < CfgData.nodesMax; i++) 
////				if (imuExtractor[i] != null && imuExtractor[i].isConnecting())
////					imuExtractor[i].close();
////			
////			if (mNodesHandler[0] != null) {
////				mNodesHandler[0].post(new Runnable(){ public void run() {
////					Toast.makeText(mContext, "Connection aborted", Toast.LENGTH_SHORT).show();
////				}});
////			}
////		}
////		eu.cupid.abf.Framework.FSM.Message cMessage;
////		cMessage.arg1 = mNodesHandler[0].BatteryValue;
////		cMessage.what = FSM.Message.END_OF_ROUTINE.ordinal();
////		FSM.handle(cMessage);
////		FSM.handle(FSM.Message.END_OF_ROUTINE);
//		
////		for (int i = 0; i < CfgData.nodesMax; i++) 
////			if (imuExtractor[i] != null)
////				BattVals[i] = mNodesHandler[i].BatteryValue;
////		
////		FSM.getBattVal(BattVals);
////		
//		
////		FSM.handle(FSM.Message.CHECK_CONNECTION);
//	}
	
	
	/** 
	 * generates imuExtractor from specified BT device
	 * @param address the MAC address of BT node
	 * @param nodeInd the index of generated ImuExtractor
	 */
//	public static synchronized void connectBTDevice(String address, int nodeInd) {
//			if (imuExtractor[nodeInd] == null) {
//				imuExtractor[nodeInd] = new ImuBTExtractor(address, mNodesHandler[nodeInd]);
//				imuExtractor[nodeInd].connect();
//				saveDevices();
//			} else if (!(imuExtractor[nodeInd].isConnected() | imuExtractor[nodeInd].isConnecting())) {
////			} else if (!(imuExtractor[nodeInd].isConnected() )) {
//				imuExtractor[nodeInd].close();
//				imuExtractor[nodeInd] = new ImuBTExtractor(address, mNodesHandler[nodeInd]);
//				imuExtractor[nodeInd].connect();
//				saveDevices();
//			}
//	}
	
	/**
	 * Clears connection mapping data
	 * @return true if connection configuration file was successfully deleted; false otherwise
	 */
	public static synchronized boolean clearSavedDevices() {
		if (mContext.deleteFile(SerializableBTDevices.fileName)) {
			Toast.makeText(mContext, "Data Cleared", Toast.LENGTH_SHORT).show();
			return true;
		} else {
			Toast.makeText(mContext, "Data not Found", Toast.LENGTH_SHORT).show();
			return false;
		}
		
	}
	
//	
//	public static synchronized int nStreamingNodes() {
//		int n = 0;
//		for (int i = 0; i < imuExtractor.length; i++) 
//			if (imuExtractor[i] != null && imuExtractor[i].isStreaming())
//				n++;
//		return n;
//	}
	
	/** 
	 * @return an array with indexes of connected nodes
	 */
//	public static synchronized int[] getConnectionsList() {
//		ArrayList<Integer> list = new ArrayList<Integer>();
//		for (int i = 0; i < imuExtractor.length; i++) 
//			if (imuExtractor[i] != null && imuExtractor[i].isConnected())
//				list.add(i);
//		int[] res = new int[list.size()];
//		for (int i = 0 ; i < list.size(); i++)
//			res[i] = list.get(i);
//		return res;
//	}
	

	
	/** 
	 * @return global number of connected nodes
	 */
	public static synchronized int nConnectedNodes() {
		return MainActivity.getnConnectedNodes();
	}
	
	/** 
	 * @return true if every node is connected
	 */
//	public static synchronized boolean isConnecting() {
//		if (imuExtractor != null) {
//			for (int i = 0; i < imuExtractor.length; i++) 
//				if (imuExtractor != null && imuExtractor[i] != null && imuExtractor[i].isConnecting())
//					return true;
//		}
//		return false; 
//	}


	/** 
	 * This method determines if global connection status is 'connected'  
	 * @return true if connection is OK
	 */
	public static synchronized boolean isConnected() {
		return true;
//		if (FSM.getMode() == FSM.MODE_ADMIN) {
//			return isMinConnected();  
//		} else if (FSM.getMode() == FSM.MODE_USER) {
//			if (CalibrationManager.accCalib != null && CalibrationManager.accCalib.isValid()) {
//				return (imuExtractor != null && 
//						imuExtractor[CfgData.nilf] != null && imuExtractor[CfgData.nilf].isConnected() &&
//						imuExtractor[CfgData.nirf] != null && imuExtractor[CfgData.nirf].isConnected() &&
//						!(imuExtractor[CfgData.nit] != null && !imuExtractor[CfgData.nit].isConnected())); //if third node is mapped and it's calibration data is present it must be connected
//			} else {
//				return isMinConnected(); 
//			}
//		} else return false;
//		
	}
	
	/** 
	 * @return true if every node is connected
	 */
	public static synchronized boolean isAllConnected() {
//		return nConnectedNodes() >= CfgData.nodesMax;  
		return true;
		//TODO this is just a stub
	}
	
	
	/**
	 * @return true if at least one node (any node) is connected
	 */
	public static synchronized boolean isAnyConnected() {
		return nConnectedNodes() > 0;
	}
	
//	/**
//	 * @return true if there are enough connected nodes for a trial run (i.e.: feet's nodes are connected)
//	 */
//	public static synchronized boolean isMinConnected() {
//		if (imuExtractor == null || imuExtractor[CfgData.nilf] == null || imuExtractor[CfgData.nirf] == null)
//			return false;
//		return imuExtractor[CfgData.nilf].isConnected() && imuExtractor[CfgData.nirf].isConnected();
//	}
	
	/**
	 * @return false if at least one node (any node) is connected
	 */
	public static synchronized boolean isNoneConnected() {
		return nConnectedNodes() == 0;
	}
	
//	/**
//	 * begins data streaming from all connected nodes
//	 */
//	public static synchronized void startAll() {
//		long time = SystemClock.elapsedRealtime();
//		//		for (ImuExtractor extractor : imuExtractor) 
//		//			if (extractor != null && extractor.isConnected())
//		//				extractor.start(time);
//		for (int i = 0; i<imuExtractor.length; i++ ) 
//			if (imuExtractor[i] != null && imuExtractor[i].isConnected())
//				imuExtractor[i].start(time);
//	}
	
//	/**
//	 * Pause data streaming from all nodes
//	 */
//	public static synchronized void  pauseAll() {
//		for (ImuExtractor extractor : imuExtractor) 
//			if (extractor != null && extractor.isStreaming())
//				extractor.pause();
//	}
	
	/**
	 * connect all devices
	 */
	public static synchronized void  connectAll() {
//		for (ImuExtractor extractor : imuExtractor) 
//			if (extractor != null && !extractor.isConnected())
//				extractor.connect();
	}


	/**
	 * closes all connections
	 */
	public static synchronized void  closeAll() {
		for (int i = 0; i < MainActivity.MaxNodes; i++) {
			BTservice[i].stop();
		}
//		for (int i = 0; i < imuExtractor.length; i++) {
//			if (imuExtractor[i] != null) {
//				imuExtractor[i].close();
//				imuExtractor[i] = null;
//			}
//		}
	}
	
	/**
	 * Saves devices' MAC addresses for easier connection restoring
	 */
	public static void saveDevices(){
		SerializableBTDevices obj = new SerializableBTDevices(nConnectedNodes());
		for (int i = 0; i < nConnectedNodes(); i++) {
			if(BTservice[i].getDeviceID() != "")
				obj.add(BTservice[i].getDeviceID(), i);
//			if (imuExtractor[i] != null) 
//				obj.add(imuExtractor[i].targetID, i);
		}
		try {
			ObjectOutputStream stream = new ObjectOutputStream(mContext.openFileOutput(SerializableBTDevices.fileName, 0));
			stream.writeObject(obj);
			stream.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/** 
	 * Gets the list of saved nodes' indexes
	 * @return the obtained list.
	 */
	public static ArrayList<Integer> getSavedList(){
		SerializableBTDevices obj;
		ArrayList<Integer> list = new ArrayList<Integer>();
		
		try {
			ObjectInputStream stream = new ObjectInputStream(mContext.openFileInput(SerializableBTDevices.fileName));
			obj = (SerializableBTDevices) stream.readObject();
			stream.close();
		} catch (Exception e) {
			e.printStackTrace();
			return list;
		} 
		
		for (int i = 0; i < obj.nobj; i++) {
			list.add(obj.nodeInd[i]);
		}
		return list;
	}
	
	/**
	 * Restores saved devices (without connecting them)
	 * @return true if devices data was found; false otherwise
	 */
	public static boolean restoreDevices() {
		return restoreBTDevices();
	}
	
	/**
	 * Restores to saved devices
	 * @return true if data was found; false otherwise.
	 */
	public static boolean restoreBTDevices(){
		SerializableBTDevices obj;

		try {
			ObjectInputStream stream = new ObjectInputStream(mContext.openFileInput(SerializableBTDevices.fileName));
			obj = (SerializableBTDevices) stream.readObject();
			stream.close();
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		} 

//		if (imuExtractor == null)
//			imuExtractor = new ImuExtractor[CfgData.nodesMax];

		int nodeInd;
		String address;
		
		for (int i = 0; i < obj.nobj; i++) {
			nodeInd = obj.nodeInd[i];
			address = obj.address[i];
			if(BTservice[i]!=null || !BTservice[i].IsConnected || !BTservice[i].IsConnecting ){
				BluetoothDevice device = BluetoothAdapter.getDefaultAdapter().getRemoteDevice(address);
				BTservice[i].connect(device, false);
			}
				
//			if (imuExtractor[nodeInd] == null  || !(imuExtractor[nodeInd].isConnected() | imuExtractor[nodeInd].isConnecting())) 
//				if (BluetoothAdapter.checkBluetoothAddress(address))
//					imuExtractor[nodeInd] = new ImuBTExtractor(address, mNodesHandler[nodeInd]);
		}
		
		return true;
	}
	


	/**
	 * Inner class used for connections save/restore purposes
	 */
	static class SerializableBTDevices implements Serializable {
		private static final long serialVersionUID = 2L; //increment every time this class is modified
		
		public static String fileName = "bt_devices";
		public int nobj = 0;
		public int[] nodeInd;
		public String[] address;
		
		
		SerializableBTDevices(int n) {
			nobj = 0;
			nodeInd = new int[n];
			address = new String[n];
		}
		
		public void add(String target, int ind) {
			nodeInd[ind] = ind;
			address[ind] = target;
			nobj++;		
		}
	}
}

