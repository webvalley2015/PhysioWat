/*
 * Copyright (C) 2009 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.niklas.datalogging;


import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.UUID;

//import com.example.android.BluetoothChat.BluetoothChat;


import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;

/**
 * This class does all the work for setting up and managing Bluetooth
 * connections with other devices. It has a thread that listens for
 * incoming connections, a thread for connecting with a device, and a
 * thread for performing data transmissions when connected.
 */
 public class BluetoothChatService {
    // Debugging
    private static final String TAG = "BluetoothChatService";
    private static final boolean D = true;

    // Name for the SDP record when creating server socket
    private static final String NAME_SECURE = "BluetoothChatSecure";
    private static final String NAME_INSECURE = "BluetoothChatInsecure";

    // Unique UUID for this application
    private static final UUID MY_UUID_SECURE =
        UUID.fromString("fa87c0d0-afac-11de-8a39-0800200c9a66");
    private static final UUID MY_UUID_INSECURE =
        UUID.fromString("00001101-0000-1000-8000-00805f9b34fb");

    // Member fields
    private final BluetoothAdapter mAdapter;
    private final Handler mHandler;
    private AcceptThread mSecureAcceptThread;
    private AcceptThread mInsecureAcceptThread;
    private ConnectThread mConnectThread;
    private ConnectedThread mConnectedThread;
    private int mState;

    // Constants that indicate the current connection state
    public static final int STATE_NONE = 0;       // we're doing nothing
    public static final int STATE_LISTEN = 1;     // now listening for incoming connections
    public static final int STATE_CONNECTING = 2; // now initiating an outgoing connection
    public static final int STATE_CONNECTED = 3;  // now connected to a remote device
    public static final int STATE_DISCONNECTED = 4;  // Disconnected from device
    
    private int contaT, contaT_prev, flag_inertial_update;
    private int ax,ay,az,gx,gy,gz,mx,my,mz;
    private int ByteCnt = 0;
    public int test_state,test_num,temp_state ,download_process, packet_counter_global, packet_loss;
    private BufferedWriter out_log;
    
    public long  StartStremingTime;
    public boolean IsConnected = false;
    public boolean IsConnecting = false;
    private long DataReceivedTime;
    private String deviceID = "";
    public String deviceName = "";

    private streamDecoder decoder;
    /**
     * Constructor. Prepares a new BluetoothChat session.
     * @param context  The UI Activity Context
     * @param handler  A Handler to send messages back to the UI Activity
     */
    public BluetoothChatService(Context context, Handler handler) {
        mAdapter = BluetoothAdapter.getDefaultAdapter();
        mState = STATE_NONE;
        mHandler = handler;
    }

    /**
     * Set the current state of the chat connection
     * @param state  An integer defining the current connection state
     */
    private synchronized void setState(int state) {
        if (D) Log.d(TAG, "setState() " + mState + " -> " + state);
        mState = state;

        // Give the new state to the Handler so the UI Activity can update
        mHandler.obtainMessage(MainActivity.MESSAGE_STATE_CHANGE, state, -1).sendToTarget();
    }

    /**
     * Return the current connection state. */
    public synchronized int getState() {
        return mState;
    }
    
    public void setOutFile(BufferedWriter outFile){
    	out_log = outFile;
    	decoder.setOutFile(out_log);
    }

    /**
     * Start the chat service. Specifically start AcceptThread to begin a
     * session in listening (server) mode. Called by the Activity onResume() */
    public synchronized void start() {
        if (D) Log.d(TAG, "start");

        // Cancel any thread attempting to make a connection
        if (mConnectThread != null) {mConnectThread.cancel(); mConnectThread = null;}

        // Cancel any thread currently running a connection
        if (mConnectedThread != null) {mConnectedThread.cancel(); mConnectedThread = null;}

//        setState(STATE_LISTEN);
//
//        // Start the thread to listen on a BluetoothServerSocket
//        if (mSecureAcceptThread == null) {
//            mSecureAcceptThread = new AcceptThread(true);
//            mSecureAcceptThread.start();
//        }
//        if (mInsecureAcceptThread == null) {
//            mInsecureAcceptThread = new AcceptThread(false);
//            mInsecureAcceptThread.start();
//        }
    }

    /**
     * Start the ConnectThread to initiate a connection to a remote device.
     * @param device  The BluetoothDevice to connect
     * @param secure Socket Security type - Secure (true) , Insecure (false)
     */
    public synchronized void connect(BluetoothDevice device, boolean secure) {
        if (D) Log.d(TAG, "connect to: " + device);

        // Cancel any thread attempting to make a connection
        if (mState == STATE_CONNECTING) {
            if (mConnectThread != null) {mConnectThread.cancel(); mConnectThread = null;}
        }

        // Cancel any thread currently running a connection
        if (mConnectedThread != null) {mConnectedThread.cancel(); mConnectedThread = null;}

        // Start the thread to connect with the given device
        mConnectThread = new ConnectThread(device, secure);
        mConnectThread.start();
        setState(STATE_CONNECTING);
    }

    /**
     * Start the ConnectedThread to begin managing a Bluetooth connection
     * @param socket  The BluetoothSocket on which the connection was made
     * @param device  The BluetoothDevice that has been connected
     */
    public synchronized void connected(BluetoothSocket socket, BluetoothDevice
            device, final String socketType) {
        if (D) Log.d(TAG, "connected, Socket Type:" + socketType);

        // Cancel the thread that completed the connection
        if (mConnectThread != null) {mConnectThread.cancel(); mConnectThread = null;}

        // Cancel any thread currently running a connection
        if (mConnectedThread != null) {mConnectedThread.cancel(); mConnectedThread = null;}

        // Cancel the accept thread because we only want to connect to one device
        if (mSecureAcceptThread != null) {
            mSecureAcceptThread.cancel();
            mSecureAcceptThread = null;
        }
        if (mInsecureAcceptThread != null) {
            mInsecureAcceptThread.cancel();
            mInsecureAcceptThread = null;
        }

        // Start the thread to manage the connection and perform transmissions
        mConnectedThread = new ConnectedThread(socket, socketType);
        mConnectedThread.start();

        // Send the name of the connected device back to the UI Activity
        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_DEVICE_NAME);
        Bundle bundle = new Bundle();
        bundle.putString(MainActivity.DEVICE_NAME, device.getName());
        msg.setData(bundle);
        mHandler.sendMessage(msg);
        deviceID = device.getAddress();
        deviceName = device.getName();
        setState(STATE_CONNECTED);
        IsConnected = true;
    }

    /**
     * Stop all threads
     */
    public synchronized void stop() {
        if (D) Log.d(TAG, "stop");

        if (mConnectThread != null) {
            mConnectThread.cancel();
            mConnectThread = null;
        }

        if (mConnectedThread != null) {
            mConnectedThread.cancel();
            mConnectedThread = null;
        }

        if (mSecureAcceptThread != null) {
            mSecureAcceptThread.cancel();
            mSecureAcceptThread = null;
        }

        if (mInsecureAcceptThread != null) {
            mInsecureAcceptThread.cancel();
            mInsecureAcceptThread = null;
        }
        setState(STATE_NONE);
    }

    /**
     * Write to the ConnectedThread in an unsynchronized manner
     * @param out The bytes to write
     * @see ConnectedThread#write(byte[])
     */
    public void write(byte[] out) {
        // Create temporary object
        ConnectedThread r;
        // Synchronize a copy of the ConnectedThread
        synchronized (this) {
            if (mState != STATE_CONNECTED) return;
            r = mConnectedThread;
        }
        // Perform the write unsynchronized
        r.write(out);
    }

    /**
     * Indicate that the connection attempt failed and notify the UI Activity.
     */
    private void connectionFailed() {
        // Send a failure message back to the Activity
        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_TOAST);
        Bundle bundle = new Bundle();
        bundle.putString(MainActivity.TOAST, "Unable to connect device");
        msg.setData(bundle);
        mHandler.sendMessage(msg);
        IsConnected = false;
        setState(STATE_DISCONNECTED);
        // Start the service over to restart listening mode
        BluetoothChatService.this.start();
    }

    /**
     * Indicate that the connection was lost and notify the UI Activity.
     */
    private void connectionLost() {
        // Send a failure message back to the Activity
        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_TOAST);
        Bundle bundle = new Bundle();
        bundle.putString(MainActivity.TOAST, "Device connection was lost");
        msg.setData(bundle);
        mHandler.sendMessage(msg);
        deviceID = "";
        deviceName = "";
        IsConnected = false;
        stop();
        setState(STATE_DISCONNECTED);
        
        
        // Start the service over to restart listening mode
        // BluetoothChatService.this.start();
    }
public String getDeviceID(){
	return deviceID;
}


    /**
     * This thread runs while listening for incoming connections. It behaves
     * like a server-side client. It runs until a connection is accepted
     * (or until cancelled).
     */
    private class AcceptThread extends Thread {
        // The local server socket
        private final BluetoothServerSocket mmServerSocket;
        private String mSocketType;

        public AcceptThread(boolean secure) {
            BluetoothServerSocket tmp = null;
            mSocketType = secure ? "Secure":"Insecure";

            // Create a new listening server socket
            try {
                if (secure) {
                    tmp = mAdapter.listenUsingRfcommWithServiceRecord(NAME_SECURE,
                        MY_UUID_SECURE);
                } else {
                    tmp = mAdapter.listenUsingInsecureRfcommWithServiceRecord(
                            NAME_INSECURE, MY_UUID_INSECURE);
                }
            } catch (IOException e) {
                Log.e(TAG, "Socket Type: " + mSocketType + "listen() failed", e);
            }
            mmServerSocket = tmp;
        }

        public void run() {
            if (D) Log.d(TAG, "Socket Type: " + mSocketType +
                    "BEGIN mAcceptThread" + this);
            setName("AcceptThread" + mSocketType);

            BluetoothSocket socket = null;

            // Listen to the server socket if we're not connected
            while (mState != STATE_CONNECTED) {
                try {
                    // This is a blocking call and will only return on a
                    // successful connection or an exception
                    socket = mmServerSocket.accept();
                } catch (IOException e) {
                    Log.e(TAG, "Socket Type: " + mSocketType + "accept() failed", e);
                    break;
                }

                // If a connection was accepted
                if (socket != null) {
                    synchronized (BluetoothChatService.this) {
                        switch (mState) {
//                        case STATE_LISTEN:
                        case STATE_CONNECTING:
                            // Situation normal. Start the connected thread.
                            connected(socket, socket.getRemoteDevice(),
                                    mSocketType);
                            break;
                        case STATE_NONE:
                        case STATE_CONNECTED:
                            // Either not ready or already connected. Terminate new socket.
                            try {
                                socket.close();
                            } catch (IOException e) {
                                Log.e(TAG, "Could not close unwanted socket", e);
                            }
                            break;
                        }
                    }
                }
            }
            if (D) Log.i(TAG, "END mAcceptThread, socket Type: " + mSocketType);

        }

        public void cancel() {
            if (D) Log.d(TAG, "Socket Type" + mSocketType + "cancel " + this);
            try {
                mmServerSocket.close();
            } catch (IOException e) {
                Log.e(TAG, "Socket Type" + mSocketType + "close() of server failed", e);
            }
        }
    }


    /**
     * This thread runs while attempting to make an outgoing connection
     * with a device. It runs straight through; the connection either
     * succeeds or fails.
     */
    private class ConnectThread extends Thread {
        private final BluetoothSocket mmSocket;
        private final BluetoothDevice mmDevice;
        private String mSocketType;

        public ConnectThread(BluetoothDevice device, boolean secure) {
            mmDevice = device;
            BluetoothSocket tmp = null;
            mSocketType = secure ? "Secure" : "Insecure";

            // Get a BluetoothSocket for a connection with the
            // given BluetoothDevice
            try {
                if (secure) {
                    tmp = device.createRfcommSocketToServiceRecord(
                            MY_UUID_SECURE);
                } else {
                    tmp = device.createInsecureRfcommSocketToServiceRecord(
                            MY_UUID_INSECURE);
                }
            } catch (IOException e) {
                Log.e(TAG, "Socket Type: " + mSocketType + "create() failed", e);
            }
            mmSocket = tmp;
        }

        public void run() {
            Log.i(TAG, "BEGIN mConnectThread SocketType:" + mSocketType);
            setName("ConnectThread" + mSocketType);

            // Always cancel discovery because it will slow down a connection
            mAdapter.cancelDiscovery();

            // Make a connection to the BluetoothSocket
            try {
                // This is a blocking call and will only return on a
                // successful connection or an exception
                mmSocket.connect();
            } catch (IOException e) {
                // Close the socket
                try {
                    mmSocket.close();
                } catch (IOException e2) {
                    Log.e(TAG, "unable to close() " + mSocketType +
                            " socket during connection failure", e2);
                }
                connectionFailed();
                return;
            }

            // Reset the ConnectThread because we're done
            synchronized (BluetoothChatService.this) {
                mConnectThread = null;
            }

            // Start the connected thread
            connected(mmSocket, mmDevice, mSocketType);
        }

        public void cancel() {
            try {
                mmSocket.close();
            } catch (IOException e) {
                Log.e(TAG, "close() of connect " + mSocketType + " socket failed", e);
            }
        }
    }

    /**
     * This thread runs during a connection with a remote device.
     * It handles all incoming and outgoing transmissions.
     */
    private class ConnectedThread extends Thread {
        private final BluetoothSocket mmSocket;
        private final InputStream mmInStream;
        private final OutputStream mmOutStream;

        public ConnectedThread(BluetoothSocket socket, String socketType) {
            Log.d(TAG, "create ConnectedThread: " + socketType);
            mmSocket = socket;
            InputStream tmpIn = null;
            OutputStream tmpOut = null;

            // Get the BluetoothSocket input and output streams
            try {
                tmpIn = socket.getInputStream();
                tmpOut = socket.getOutputStream();
            } catch (IOException e) {
                Log.e(TAG, "temp sockets not created", e);
            }

            mmInStream = tmpIn;
            mmOutStream = tmpOut;
            decoder = new streamDecoder(mmInStream, mmOutStream, mHandler);
        }

        public void run() {
            Log.i(TAG, "BEGIN mConnectedThread");
            byte[] buffer = new byte[1024];
            int bytes;
            long lastDataPlotTime = android.os.SystemClock.elapsedRealtime();
//            long currDataPlotTime = android.os.SystemClock.elapsedRealtime();
//            decoder = new streamDecoder(mmInStream, mmOutStream, mHandler);
        	try {
				bytes = mmInStream.read(buffer);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				connectionLost();
			}
            
            // Keep listening to the InputStream while connected
            while (true) {

            	while (mState == STATE_CONNECTED) {
//            		try {
//						Thread.sleep(5);
//					} catch (InterruptedException e) {
//						// TODO Auto-generated catch block
//						e.printStackTrace();
//					}
            		try {
						decoder.readData();
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
						connectionLost();
						mState = STATE_DISCONNECTED;
					}
            	}
            	
            	
            	
//                try {
//                    // Read from the InputStream
//                    bytes = mmInStream.read(buffer);
//                    
//                    // Send the obtained bytes to the UI Activity
//                    int b_tmp=0;
//                    int b_tmp_aug=0;
//                    int cnt=0;
//                    
//        			contaT=0;
//        			contaT_prev=0;
//        			long checksum=0, checksum_received=0;
//        			flag_inertial_update=0;
//                   
//                    	cnt=0;
//                    	//flag=0;
//                    	while (mState == STATE_CONNECTED) {
//                    		try{
//                    			// Read from the InputStream
//                    			cnt=0;
//                    			
//                    		b_tmp=(int)mmInStream.read();
//                    		if (b_tmp == 0x20 && ConfigVals.nodeType != ConfigVals.GENERIC_NODE) {//
//                    				b_tmp_aug=(int)mmInStream.read();
//                    			if (b_tmp_aug == 0x0A||b_tmp_aug == 0x0B) {
//                    				try {
//                    					DataReceivedTime =android.os.SystemClock.elapsedRealtime();
//                    					buffer[cnt] = (byte)b_tmp;//b_tmp[0];
//                    					//out.writeByte(buffer[cnt]);
//                    					cnt++;
//                    					buffer[cnt] = (byte)b_tmp_aug;//b_tmp[0];
//                    					cnt++;
//
//                    					while (cnt < 22) { //
//                    						b_tmp = mmInStream.read();//mmInStream.read(b_tmp);//.read();//
//                    						buffer[cnt] = (byte)b_tmp;//b_tmp[0];
//                    						cnt++;
//                    					}
//                    					
//                    					
//                    					if(buffer[0]==0x20 && (buffer[1]==0x0A ||buffer[1]==0x0B)){
//                    						           						
//                    						contaT = ((int)buffer[2]&0xFF);// (int)(buffer[indiceS + 2]);
//                    						
//                    						ax = (short)((buffer[3]&0xFF)+((buffer[4]&0xFF)*256));
//                    						ay = (short)((buffer[5]&0xFF)+((buffer[6]&0xFF)*256));            						
//                    						az = (short)((buffer[7]&0xFF)+((buffer[8]&0xFF)*256));
//
//                    						gx = (short)((buffer[9]&0xFF) +((buffer[10]&0xFF)*256));
//                    						gy = (short)((buffer[11]&0xFF) +((buffer[12]&0xFF)*256));
//                    						gz = (short)((buffer[13]&0xFF) +((buffer[14]&0xFF)*256));
//                    						
//                    						mx = (short)((buffer[15]&0xFF) +((buffer[16]&0xFF)*256));
//                    						my = (short)((buffer[17]&0xFF) +((buffer[18]&0xFF)*256));
//                    						mz = (short)((buffer[19]&0xFF) +((buffer[20]&0xFF)*256));
//
//                    						checksum_received = ((int)buffer[21]&0xFF);
//                    						
//                    						if (contaT % 100 == 43) //necessary to avoid that newer version of Android (4.3+) closes the connection 
//                                    			mmOutStream.write('=');
//                    						
//                    						for (int j=0; j<21; j++)
//                    							checksum = checksum ^ ((int)buffer[j]& 0xFF);// (int)(dataBuffer[j] + (u16)(dataBuffer[j+1]<<8));
//                    						     						
//                    						
//                    						if (checksum_received==checksum){
//                    							
//                    							flag_inertial_update=1;
//                    							if (test_state==1 || test_state==2){
//                    								temp_state--;
//                    								if (temp_state==0)
//                    									test_state=0;
//                    							}else
//                    								temp_state=20;
//                    					        
//                    							try{
//                    								if (download_process==0){
//                    									
//                    									out_log.write(DataReceivedTime+" ;"+contaT+";"+ax+";"+ay+";"+az+";"+gx+";"+gy+";"+gz+";"+mx+";"+my+";"+mz+";"+checksum_received+";"+checksum/*+";"+test_num+";"+test_state*/+";\n");
//                    									out_log.flush();
//                    								}else if (download_process==1){
//                    								}
//                    								
//                    							} catch (IOException e) {
//                    								// TODO Auto-generated catch block
//                    								e.printStackTrace();
//                    							}
//                    							
//                    							packet_counter_global++;
//                    							
//                    						 	if (packet_counter_global>1000){
//                    						 		//check number packet loss
//                    							 	if ((contaT - contaT_prev)>1){
//                    									packet_loss++;
//                    								}
//                    							 
//                    							}
//                    							contaT_prev=contaT;
//                    						}
//                    					}
//                    					checksum=0;
//                    				} catch (IOException e1) {
//                    					// TODO Auto-generated catch block
//                            			//connectionLost();
//                    					e1.printStackTrace();
//                    					
//                    				}
//                    				
//                   				// Send the obtained bytes to the UI Activity
//                    				float[] echoMsg;
//                    				echoMsg = new float[10];
//                    				echoMsg[0] = ax;
//                    				echoMsg[1] = ay;
//                    				echoMsg[2] = az;
//                    				echoMsg[3] = gx;
//                    				echoMsg[4] = gy;
//                    				echoMsg[5] = gz;                    				
//                    				echoMsg[9] = packet_loss;
////                    				if ( (contaT % 20 == 0)){
//                    				if (DataReceivedTime - lastDataPlotTime > ConfigVals.plotInterval ){
//                    					lastDataPlotTime = DataReceivedTime;
//                    			        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_READ);
//                    			        Bundle bundle = new Bundle();
//                    			        bundle.putFloatArray(MainActivity.SENS_DATA, echoMsg);
//                    			        msg.setData(bundle);
//                    			        mHandler.sendMessage(msg);
////                    			        
////	                    				mHandler.obtainMessage(MainActivity.MESSAGE_READ, 1, -1,
////	                    						echoMsg).sendToTarget();
//                    				}
//
//                    			}
//                    			else if (b_tmp_aug == 0x0C){
//                    				int q1,q2,q3,q4;
//                    				try {
//                    					DataReceivedTime =android.os.SystemClock.elapsedRealtime();
//                    					buffer[cnt] = (byte)b_tmp;//b_tmp[0];
//                    					//out.writeByte(buffer[cnt]);
//                    					cnt++;
//                    					buffer[cnt] = (byte)b_tmp_aug;//b_tmp[0];
//                    					cnt++;
//                    					int packetSize = 20;
//                    					while (cnt < packetSize) { //
//                    						b_tmp = mmInStream.read();//mmInStream.read(b_tmp);//.read();//
//                    						buffer[cnt] = (byte)b_tmp;//b_tmp[0];
//                    						cnt++;
//                    					}
//                    					
//                    					
//                    					if(buffer[0]==0x20 && buffer[1]==0x0C){
//                    						           						
//                    						contaT = ((int)buffer[2]&0xFF);// (int)(buffer[indiceS + 2]);
//                    						
//                    						q1 = (int)((buffer[3]&0xFF)+((buffer[4]&0xFF)*256) + ((buffer[5]&0xFF)*256*256) + ((buffer[6]&0xFF)*256*256*256) );
//                    						q2 = (int)((buffer[7]&0xFF)+((buffer[8]&0xFF)*256) + ((buffer[9]&0xFF)*256*256) + ((buffer[11]&0xFF)*256*256*256) );           						
//                    						q3 = (int)((buffer[11]&0xFF)+((buffer[12]&0xFF)*256) + ((buffer[13]&0xFF)*256*256) + ((buffer[14]&0xFF)*256*256*256) );
//                    						q4 = (int)((buffer[15]&0xFF)+((buffer[16]&0xFF)*256) + ((buffer[17]&0xFF)*256*256) + ((buffer[18]&0xFF)*256*256*256) );
//                    						
//                    						checksum_received = ((int)buffer[19]&0xFF);//+(((int)buffer[22]& 0xFF)<<8); //(ushort)(buffer[indiceS + 21] + ((buffer[indiceS + 22]) << 8));
//                
//                    						if (contaT % 100 == 43) //necessary to avoid that newer version of Android (4.3+) closes the connection 
//                                    			mmOutStream.write('=');
//                    						
//                    						for (int j=0; j<packetSize-1; j++)
//                    							checksum = checksum ^ ((int)buffer[j]& 0xFF);// (int)(dataBuffer[j] + (u16)(dataBuffer[j+1]<<8));
//                    						     						
//                    						
//                    						if (checksum_received==checksum){
//                    							flag_inertial_update=1;
//                    							try{
//                    								if (download_process==0){
//                    									out_log.write(DataReceivedTime+" ;"+contaT+";"+q1+";"+q2+";"+q3+";"+q4+";\n");
//                    									out_log.flush();
//                    								}else if (download_process==1){
//                    								}
//                    								
//                    							} catch (IOException e) {
//                    								// TODO Auto-generated catch block
//                    								e.printStackTrace();
//                    							}
//                    							
//                    							packet_counter_global++;
//                    							
//                    						 	if (packet_counter_global>1000){
//                    						 		//check number packet loss
//                    							 	if ((contaT - contaT_prev)>1){
//                    									packet_loss++;
//                    								}
//                    							 
//                    							}
//                    							contaT_prev=contaT;
//                    						}
//                    					}
//                    					checksum=0;
//                    				} catch (IOException e1) {
//                    					// TODO Auto-generated catch block
//                            			//connectionLost();
//                    					e1.printStackTrace();
//                    					
//                    				}
//                    				
//                   				// Send the obtained bytes to the UI Activity
////                    				float[] echoMsg;
////                    				echoMsg = new float[10];
////                    				echoMsg[0] = ax;
////                    				echoMsg[1] = ay;
////                    				echoMsg[2] = az;
////                    				echoMsg[3] = gx;
////                    				echoMsg[4] = gy;
////                    				echoMsg[5] = gz;                    				
////                    				echoMsg[9] = packet_loss;
//////                    				if ( (contaT % 20 == 0)){
////                    				if (DataReceivedTime - lastDataPlotTime > ConfigVals.plotInterval ){
////                    					lastDataPlotTime = DataReceivedTime;
////                    			        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_READ);
////                    			        Bundle bundle = new Bundle();
////                    			        bundle.putFloatArray(MainActivity.SENS_DATA, echoMsg);
////                    			        msg.setData(bundle);
////                    			        mHandler.sendMessage(msg);
////                    				}
//
//                    			}
//                    			
//                    			else if (b_tmp_aug == 0x0D){
//                    				
//                    				int q1,q2,q3,q4;
//                    				try {
//                    					DataReceivedTime =android.os.SystemClock.elapsedRealtime();
//                    					buffer[cnt] = (byte)b_tmp;//b_tmp[0];
//                    					//out.writeByte(buffer[cnt]);
//                    					cnt++;
//                    					buffer[cnt] = (byte)b_tmp_aug;//b_tmp[0];
//                    					cnt++;
//                    					int packetSize = 38;
//                    					while (cnt < packetSize) { //
//                    						b_tmp = mmInStream.read();//mmInStream.read(b_tmp);//.read();//
//                    						buffer[cnt] = (byte)b_tmp;//b_tmp[0];
//                    						cnt++;
//                    					}
//                    					
//                    					
//                    					if(buffer[0]==0x20 && buffer[1]==0x0D){
//                    						           						
//                    						contaT = ((int)buffer[2]&0xFF);// (int)(buffer[indiceS + 2]);
//                    						ax = (short)((buffer[3]&0xFF)+((buffer[4]&0xFF)*256));
//                    						ay = (short)((buffer[5]&0xFF)+((buffer[6]&0xFF)*256));            						
//                    						az = (short)((buffer[7]&0xFF)+((buffer[8]&0xFF)*256));
//
//                    						gx = (short)((buffer[9]&0xFF) +((buffer[10]&0xFF)*256));
//                    						gy = (short)((buffer[11]&0xFF) +((buffer[12]&0xFF)*256));
//                    						gz = (short)((buffer[13]&0xFF) +((buffer[14]&0xFF)*256));
//                    						
//                    						mx = (short)((buffer[15]&0xFF) +((buffer[16]&0xFF)*256));
//                    						my = (short)((buffer[17]&0xFF) +((buffer[18]&0xFF)*256));
//                    						mz = (short)((buffer[19]&0xFF) +((buffer[20]&0xFF)*256));
//                    						
//                    						q1 = (int)((buffer[21]&0xFF)+((buffer[22]&0xFF)*256) + ((buffer[23]&0xFF)*256*256) + ((buffer[24]&0xFF)*256*256*256) );
//                    						q2 = (int)((buffer[25]&0xFF)+((buffer[26]&0xFF)*256) + ((buffer[27]&0xFF)*256*256) + ((buffer[28]&0xFF)*256*256*256) );           						
//                    						q3 = (int)((buffer[29]&0xFF)+((buffer[30]&0xFF)*256) + ((buffer[31]&0xFF)*256*256) + ((buffer[32]&0xFF)*256*256*256) );
//                    						q4 = (int)((buffer[33]&0xFF)+((buffer[34]&0xFF)*256) + ((buffer[35]&0xFF)*256*256) + ((buffer[36]&0xFF)*256*256*256) );
//                    						
//                    						checksum_received = ((int)buffer[37]&0xFF);//+(((int)buffer[22]& 0xFF)<<8); //(ushort)(buffer[indiceS + 21] + ((buffer[indiceS + 22]) << 8));
//                
//                    						if (contaT % 100 == 43) //necessary to avoid that newer version of Android (4.3+) closes the connection 
//                                    			mmOutStream.write('=');
//                    						
//                    						for (int j=0; j<packetSize-1; j++)
//                    							checksum = checksum ^ ((int)buffer[j]& 0xFF);// (int)(dataBuffer[j] + (u16)(dataBuffer[j+1]<<8));
//                    						     						
//                    						
//                    						if (checksum_received==checksum){
//                    							flag_inertial_update=1;
//                    							try{
//                    								if (download_process==0){
//                    									out_log.write(DataReceivedTime+" ;"+contaT+";"+q1+";"+q2+";"+q3+";"+q4+";\n");
//                    									out_log.flush();
//                    								}else if (download_process==1){
//                    								}
//                    								
//                    							} catch (IOException e) {
//                    								// TODO Auto-generated catch block
//                    								e.printStackTrace();
//                    							}
//                    							
//                    							packet_counter_global++;
//                    							
//                    						 	if (packet_counter_global>1000){
//                    						 		//check number packet loss
//                    							 	if ((contaT - contaT_prev)>1){
//                    									packet_loss++;
//                    								}
//                    							 
//                    							}
//                    							contaT_prev=contaT;
//                    						}
//                    					}
//                    					checksum=0;
//                    				} catch (IOException e1) {
//                    					// TODO Auto-generated catch block
//                            			//connectionLost();
//                    					e1.printStackTrace();
//                    					
//                    				}
//                    				
//                   				// Send the obtained bytes to the UI Activity
//                    				float[] echoMsg;
//                    				echoMsg = new float[10];
//                    				echoMsg[0] = ax;
//                    				echoMsg[1] = ay;
//                    				echoMsg[2] = az;
//                    				echoMsg[3] = gx;
//                    				echoMsg[4] = gy;
//                    				echoMsg[5] = gz;                    				
//                    				echoMsg[9] = packet_loss;
//                    				if (DataReceivedTime - lastDataPlotTime > ConfigVals.plotInterval ){
//                    					lastDataPlotTime = DataReceivedTime;
//                    			        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_READ);
//                    			        Bundle bundle = new Bundle();
//                    			        bundle.putFloatArray(MainActivity.SENS_DATA, echoMsg);
//                    			        msg.setData(bundle);
//                    			        mHandler.sendMessage(msg);
//                    				}
//
//                    			}
//        					}
//                    		else if(ConfigVals.nodeType == ConfigVals.GENERIC_NODE){
//                    			char[] data = new char[20];
//                    			data[0] = (char) b_tmp;
//                    			cnt++;
//                    			for (int i = 0; i< 9; i++){
//                    				data[cnt] =  (char) mmInStream.read();
//                    				cnt++;
//                    			}
//                    			
//                    			out_log.write(data,0,cnt);
//								out_log.flush();
//                    		}
//                    		}catch (IOException e){
//                    			Log.e(TAG, "disconnected", e);
//                    			connectionLost();
//                    			break;
//                    		}
//                    		if (contaT == 100)
//                    			mmOutStream.write('=');
//                    	}
//
//                } catch (IOException e) {
//                    Log.e(TAG, "disconnected", e);
//                    connectionLost();
//                    break;
//                }
            }
        }
        

        /**
         * Write to the connected OutStream.
         * @param buffer  The bytes to write
         */
        public void write(byte[] buffer) {
            try {
                mmOutStream.write(buffer);

                // Share the sent message back to the UI Activity
                mHandler.obtainMessage(MainActivity.MESSAGE_WRITE, -1, -1, buffer)
                        .sendToTarget();
            } catch (IOException e) {
                Log.e(TAG, "Exception during write", e);
            }
        }

        public void cancel() {
            try {
                mmSocket.close();
            } catch (IOException e) {
                Log.e(TAG, "close() of connect socket failed", e);
            }
        }
    }

}
