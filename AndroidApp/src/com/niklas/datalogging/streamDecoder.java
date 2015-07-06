package com.niklas.datalogging;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;

public class streamDecoder {
	private InputStream mmInStream = null;
	private OutputStream mmOutStream = null;
	private BufferedWriter out_log;
	private Handler mHandler;
	private long lastDataPlotTime;
	private byte[] buffer = new byte[512];
	private int cnt = 0;
	private long DataReceivedTime = 0;
	
	streamDecoder(InputStream iStream,OutputStream oStream, Handler appHandler ){
		mmInStream = iStream;
		mmOutStream = oStream;
		lastDataPlotTime = android.os.SystemClock.elapsedRealtime();
		mHandler = appHandler;
	}
	
	public void setOutFile(BufferedWriter logFile){
		out_log = logFile;
	}
	
	public void readData() throws IOException{
		//Read two bytes and clock timer
		buffer[cnt++]=(byte)mmInStream.read();
		DataReceivedTime =android.os.SystemClock.elapsedRealtime();
		
		if (ConfigVals.nodeType == ConfigVals.EXELs1_NODE || ConfigVals.nodeType == ConfigVals.EXELs3_NODE || ConfigVals.nodeType == ConfigVals.CEREBRO_NODE ){
			if (buffer[0] == 0x20){
				buffer[cnt++]=(byte)mmInStream.read();
				if (buffer[0] == 0x20 && buffer[1] == 0x0A) {
					decodeCupidRaw();
				}
				if (buffer[0] == 0x20 && buffer[1] == 0x0B) {
					decodeCupidCalib();
				}
				if (buffer[0] == 0x20 && buffer[1] == 0x0C) {
					decodeCupidQuat();
				}
				if (buffer[0] == 0x20 && buffer[1] == 0x0D) {
					decodeCupidQuatRaw();
				}
			}
		}else if (ConfigVals.nodeType == ConfigVals.FLORIMAGE_NODE ){
			if (buffer[0] == 0x20){
				buffer[cnt++]=(byte)mmInStream.read();
				if (buffer[1] == 0x0A) {
					decodeFSR();
					cnt = 0;
				}
			}
		}
		else if (ConfigVals.nodeType == ConfigVals.GENERIC_NODE ){
			decodeGeneric();
		}
//		else if (ConfigVals.nodeType == ConfigVals.CEREBRO_NODE ){
//			if (buffer[0] == 0x20){
//				buffer[cnt++]=(byte)mmInStream.read();
//				if (buffer[1] == 0x0A) {
//					decodeCerebro();
//				}
//				if (buffer[1] == 0x0F) {
//					decodeIMU();
//				}
//			}
//		}
		cnt = 0;
	}
	
	private void decodeGeneric() throws IOException {
		char[] data = new char[20];
		
		for (int i = 0; i< 10; i++){
			data[cnt] =  (char) mmInStream.read();
			cnt++;
		}
		
		out_log.write(data,0,cnt);
		out_log.flush();
		
	}
	
	private void decodeFSR() throws IOException {
	//	byte[] data = new byte[180];
		int packetSize = 163, contaT;
		float pres0,pres1,pres2;
		
		while (cnt < packetSize){
			buffer[cnt] =  (byte) mmInStream.read();
			cnt++;
		}
		
		contaT = ((int)buffer[2]&0xFF);
		pres0 = (short)((buffer[3]&0xFF)+((buffer[4]&0xFF)*256));
		
		out_log.write(DataReceivedTime+" ;"+contaT+";"+pres0+";\n");
		out_log.flush();
		
		
		//necessary to avoid that newer version of Android (4.3+) closes the connection 
		if (contaT % 50== 5) {
			mmOutStream.write('s');
			try {
				Thread.sleep(50);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			mmOutStream.write('s');
		}
		
		float[] echoMsg;
		echoMsg = new float[10];
		echoMsg[0] = pres0;
		echoMsg[1] = -100;
		echoMsg[2] = -100;                  				
		if (DataReceivedTime - lastDataPlotTime > ConfigVals.plotInterval ){
			lastDataPlotTime = DataReceivedTime;
	        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_READ);
	        Bundle bundle = new Bundle();
	        bundle.putFloatArray(MainActivity.SENS_DATA, echoMsg);
	        msg.setData(bundle);
	        mHandler.sendMessage(msg);

		}
		
	}
	
	
	

	private void decodeCupidQuatRaw() throws IOException {
		int packetSize = 38;
		float ax = 0,ay = 0,az = 0,gx = 0,gy = 0,gz = 0,mx,my,mz,q1,q2,q3,q4;
		int contaT,checksum = 0,checksum_received,contaT_prev = 0,packet_loss = 0, packet_counter_global = 0;
//		try {
			//read a whole packet:
			while (cnt < packetSize) { 
				buffer[cnt] = (byte) mmInStream.read();
				cnt++;
			}
			contaT = ((int)buffer[2]&0xFF);// (int)(buffer[indiceS + 2]);
			
			ax = (short)((buffer[3]&0xFF)+((buffer[4]&0xFF)*256));
			ay = (short)((buffer[5]&0xFF)+((buffer[6]&0xFF)*256));            						
			az = (short)((buffer[7]&0xFF)+((buffer[8]&0xFF)*256));

			gx = (short)((buffer[9]&0xFF) +((buffer[10]&0xFF)*256));
			gy = (short)((buffer[11]&0xFF) +((buffer[12]&0xFF)*256));
			gz = (short)((buffer[13]&0xFF) +((buffer[14]&0xFF)*256));
			
			mx = (short)((buffer[15]&0xFF) +((buffer[16]&0xFF)*256));
			my = (short)((buffer[17]&0xFF) +((buffer[18]&0xFF)*256));
			mz = (short)((buffer[19]&0xFF) +((buffer[20]&0xFF)*256));
			
			q1 = (int)((buffer[21]&0xFF)+((buffer[22]&0xFF)*256) + ((buffer[23]&0xFF)*256*256) + ((buffer[24]&0xFF)*256*256*256) );
			q2 = (int)((buffer[25]&0xFF)+((buffer[26]&0xFF)*256) + ((buffer[27]&0xFF)*256*256) + ((buffer[28]&0xFF)*256*256*256) );           						
			q3 = (int)((buffer[29]&0xFF)+((buffer[30]&0xFF)*256) + ((buffer[31]&0xFF)*256*256) + ((buffer[32]&0xFF)*256*256*256) );
			q4 = (int)((buffer[33]&0xFF)+((buffer[34]&0xFF)*256) + ((buffer[35]&0xFF)*256*256) + ((buffer[36]&0xFF)*256*256*256) );

			checksum_received = ((int)buffer[packetSize-1]&0xFF);
			
			//necessary to avoid that newer version of Android (4.3+) closes the connection 
			if (contaT % 100 == 43) 
    			mmOutStream.write('=');
			
			//Verify checksum
			for (int j=0; j<packetSize-1; j++)
				checksum = checksum ^ ((int)buffer[j]& 0xFF);


			out_log.write(DataReceivedTime+" ;"+contaT+";"+ax+";"+ay+";"+az+";"+gx+";"+gy+";"+gz+";"+mx+";"+my+";"+mz+";"+q1+";"+q2+";"+q3+";"+q4+";\n");
			out_log.flush();
			if (checksum_received==checksum){
				packet_counter_global++;

				if (packet_counter_global>1000){
					//check number packet loss
					if ((contaT - contaT_prev)>1)
						packet_loss++;					 
				}

				contaT_prev=contaT;
			}
			checksum=0;
		
		// Send the obtained bytes to the UI Activity
		float[] echoMsg;
		echoMsg = new float[10];
		echoMsg[0] = ax;
		echoMsg[1] = ay;
		echoMsg[2] = az;
		echoMsg[3] = gx;
		echoMsg[4] = gy;
		echoMsg[5] = gz;                    				
		echoMsg[9] = packet_loss;
		if (DataReceivedTime - lastDataPlotTime > ConfigVals.plotInterval ){
			lastDataPlotTime = DataReceivedTime;
	        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_READ);
	        Bundle bundle = new Bundle();
	        bundle.putFloatArray(MainActivity.SENS_DATA, echoMsg);
	        msg.setData(bundle);
	        mHandler.sendMessage(msg);

		}
		
	}

	private void decodeCupidQuat() throws IOException {
		// ExelSx node, raw data type
		int packetSize = 20;
		int q1,q2,q3,q4;
		int contaT,checksum = 0,checksum_received,contaT_prev = 0,packet_loss = 0, packet_counter_global = 0;
//		try {
			//read a whole packet:
			while (cnt < packetSize) { 
				buffer[cnt] = (byte) mmInStream.read();
				cnt++;
			}
			contaT = ((int)buffer[2]&0xFF);// (int)(buffer[indiceS + 2]);
			
			q1 = (int)((buffer[3]&0xFF)+((buffer[4]&0xFF)*256) + ((buffer[5]&0xFF)*256*256) + ((buffer[6]&0xFF)*256*256*256) );
			q2 = (int)((buffer[7]&0xFF)+((buffer[8]&0xFF)*256) + ((buffer[9]&0xFF)*256*256) + ((buffer[11]&0xFF)*256*256*256) );           						
			q3 = (int)((buffer[11]&0xFF)+((buffer[12]&0xFF)*256) + ((buffer[13]&0xFF)*256*256) + ((buffer[14]&0xFF)*256*256*256) );
			q4 = (int)((buffer[15]&0xFF)+((buffer[16]&0xFF)*256) + ((buffer[17]&0xFF)*256*256) + ((buffer[18]&0xFF)*256*256*256) );


			checksum_received = ((int)buffer[packetSize-1]&0xFF);
			
			//necessary to avoid that newer version of Android (4.3+) closes the connection 
			if (contaT % 100 == 43) 
    			mmOutStream.write('=');
			
			//Verify checksum
			for (int j=0; j<packetSize-1; j++)
				checksum = checksum ^ ((int)buffer[j]& 0xFF);
				     						
			if (checksum_received==checksum){				        
				out_log.write(DataReceivedTime+" ;"+contaT+";"+q1+";"+q2+";"+q3+";"+q4+";\n");
				out_log.flush();

				packet_counter_global++;
					
			 	if (packet_counter_global>1000){
			 		//check number packet loss
				 	if ((contaT - contaT_prev)>1)
						packet_loss++;					 
				}
				
			 	contaT_prev=contaT;
			}
			checksum=0;
		
		// Send the obtained bytes to the UI Activity
		float[] echoMsg;
		echoMsg = new float[10];                				
		echoMsg[9] = packet_loss;
		if (DataReceivedTime - lastDataPlotTime > ConfigVals.plotInterval ){
			lastDataPlotTime = DataReceivedTime;
	        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_READ);
	        Bundle bundle = new Bundle();
	        bundle.putFloatArray(MainActivity.SENS_DATA, echoMsg);
	        msg.setData(bundle);
	        mHandler.sendMessage(msg);
		}

	}
		

	private void decodeCupidRaw() throws IOException{
			// ExelSx node, raw data type
			int packetSize = 22;
			float ax = 0,ay = 0,az = 0,gx = 0,gy = 0,gz = 0,mx,my,mz;
			int contaT,checksum = 0,checksum_received,contaT_prev = 0,packet_loss = 0, packet_counter_global = 0;
//			try {
				//read a whole packet:
				while (cnt < packetSize) { 
					buffer[cnt] = (byte) mmInStream.read();
					cnt++;
				}
				contaT = ((int)buffer[2]&0xFF);// (int)(buffer[indiceS + 2]);
				
				ax = (short)((buffer[3]&0xFF)+((buffer[4]&0xFF)*256));
				ay = (short)((buffer[5]&0xFF)+((buffer[6]&0xFF)*256));            						
				az = (short)((buffer[7]&0xFF)+((buffer[8]&0xFF)*256));

				gx = (short)((buffer[9]&0xFF) +((buffer[10]&0xFF)*256));
				gy = (short)((buffer[11]&0xFF) +((buffer[12]&0xFF)*256));
				gz = (short)((buffer[13]&0xFF) +((buffer[14]&0xFF)*256));
				
				mx = (short)((buffer[15]&0xFF) +((buffer[16]&0xFF)*256));
				my = (short)((buffer[17]&0xFF) +((buffer[18]&0xFF)*256));
				mz = (short)((buffer[19]&0xFF) +((buffer[20]&0xFF)*256));

				checksum_received = ((int)buffer[packetSize-1]&0xFF);
				
				//necessary to avoid that newer version of Android (4.3+) closes the connection 
				if (contaT % 100 == 43) 
        			mmOutStream.write('=');
				
				//Verify checksum
				for (int j=0; j<packetSize-1; j++)
					checksum = checksum ^ ((int)buffer[j]& 0xFF);
					     						
					        
					out_log.write(DataReceivedTime+" ;"+contaT+";"+ax+";"+ay+";"+az+";"+gx+";"+gy+";"+gz+";"+mx+";"+my+";"+mz+";"+checksum_received+";"+checksum/*+";"+test_num+";"+test_state*/+";\n");
					out_log.flush();
				
				if (checksum_received==checksum){			
					packet_counter_global++;
						
				 	if (packet_counter_global>1000){
				 		//check number packet loss
					 	if ((contaT - contaT_prev)>1)
							packet_loss++;					 
					}
					
				 	contaT_prev=contaT;
				}
				checksum=0;

			
			// Send the obtained bytes to the UI Activity
			float[] echoMsg;
			echoMsg = new float[10];
			echoMsg[0] = ax;
			echoMsg[1] = ay;
			echoMsg[2] = az;
			echoMsg[3] = gx;
			echoMsg[4] = gy;
			echoMsg[5] = gz;                    				
			echoMsg[9] = packet_loss;
			if (DataReceivedTime - lastDataPlotTime > ConfigVals.plotInterval ){
				lastDataPlotTime = DataReceivedTime;
		        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_READ);
		        Bundle bundle = new Bundle();
		        bundle.putFloatArray(MainActivity.SENS_DATA, echoMsg);
		        msg.setData(bundle);
		        mHandler.sendMessage(msg);

			}

		}
	
	private void decodeCupidCalib() throws IOException{
			// ExelSx node, raw data type
			int packetSize = 22;
			float ax = 0,ay = 0,az = 0,gx = 0,gy = 0,gz = 0,mx,my,mz;
			int contaT,checksum = 0,checksum_received,contaT_prev = 0,packet_loss = 0, packet_counter_global = 0;
//			try {
				//read a whole packet:
				while (cnt < packetSize) { 
					buffer[cnt] = (byte) mmInStream.read();
					cnt++;
				}
				contaT = ((int)buffer[2]&0xFF);// (int)(buffer[indiceS + 2]);
				
				ax = (short)((buffer[3]&0xFF)+((buffer[4]&0xFF)*256));
				ay = (short)((buffer[5]&0xFF)+((buffer[6]&0xFF)*256));            						
				az = (short)((buffer[7]&0xFF)+((buffer[8]&0xFF)*256));

				gx = (short)((buffer[9]&0xFF) +((buffer[10]&0xFF)*256));
				gy = (short)((buffer[11]&0xFF) +((buffer[12]&0xFF)*256));
				gz = (short)((buffer[13]&0xFF) +((buffer[14]&0xFF)*256));
				
				mx = (short)((buffer[15]&0xFF) +((buffer[16]&0xFF)*256));
				my = (short)((buffer[17]&0xFF) +((buffer[18]&0xFF)*256));
				mz = (short)((buffer[19]&0xFF) +((buffer[20]&0xFF)*256));

				checksum_received = ((int)buffer[21]&0xFF);
				
				//necessary to avoid that newer version of Android (4.3+) closes the connection 
				if (contaT % 100 == 43) 
        			mmOutStream.write('=');
				
				//Verify checksum
				for (int j=0; j<packetSize-1; j++)
					checksum = checksum ^ ((int)buffer[j]& 0xFF);
					     						
				if (checksum_received==checksum){				        
					out_log.write(DataReceivedTime+" ;"+contaT+";"+ax+";"+ay+";"+az+";"+gx+";"+gy+";"+gz+";"+mx+";"+my+";"+mz+";"+checksum_received+";"+checksum/*+";"+test_num+";"+test_state*/+";\n");
					out_log.flush();

					packet_counter_global++;
						
				 	if (packet_counter_global>1000){
				 		//check number packet loss
					 	if ((contaT - contaT_prev)>1)
							packet_loss++;					 
					}
					
				 	contaT_prev=contaT;
				}
				checksum=0;
			
			// Send the obtained bytes to the UI Activity
			float[] echoMsg;
			echoMsg = new float[10];
			echoMsg[0] = ax;
			echoMsg[1] = ay;
			echoMsg[2] = az;
			echoMsg[3] = gx;
			echoMsg[4] = gy;
			echoMsg[5] = gz;                    				
			echoMsg[9] = packet_loss;
			if (DataReceivedTime - lastDataPlotTime > ConfigVals.plotInterval ){
				lastDataPlotTime = DataReceivedTime;
		        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_READ);
		        Bundle bundle = new Bundle();
		        bundle.putFloatArray(MainActivity.SENS_DATA, echoMsg);
		        msg.setData(bundle);
		        mHandler.sendMessage(msg);

			}

		}
	
	
	
	private void decodeIMU() throws IOException{
		// ExelSx node, raw data type
		int packetSize = 22;
		int ax = 0,ay = 0,az = 0,gx = 0,gy = 0,gz = 0,mx,my,mz;
		int contaT,checksum = 0,checksum_received,contaT_prev = 0,packet_loss = 0, packet_counter_global = 0;
//		try {
			//read a whole packet:
			while (cnt < packetSize) { 
				buffer[cnt] = (byte) mmInStream.read();
				cnt++;
			}
			contaT = ((int)buffer[2]&0xFF);// (int)(buffer[indiceS + 2]);
			
			ax = (short)((buffer[3]&0xFF)+((buffer[4]&0xFF)*256));
			ay = (short)((buffer[5]&0xFF)+((buffer[6]&0xFF)*256));            						
			az = (short)((buffer[7]&0xFF)+((buffer[8]&0xFF)*256));

			gx = (short)((buffer[9]&0xFF) +((buffer[10]&0xFF)*256));
			gy = (short)((buffer[11]&0xFF) +((buffer[12]&0xFF)*256));
			gz = (short)((buffer[13]&0xFF) +((buffer[14]&0xFF)*256));
			
			mx = (short)((buffer[15]&0xFF) +((buffer[16]&0xFF)*256));
			my = (short)((buffer[17]&0xFF) +((buffer[18]&0xFF)*256));
			mz = (short)((buffer[19]&0xFF) +((buffer[20]&0xFF)*256));

			checksum_received = ((int)buffer[packetSize-1]&0xFF);
			
			//necessary to avoid that newer version of Android (4.3+) closes the connection 
			if (contaT % 100 == 43) 
    			mmOutStream.write('=');
			
			//Verify checksum
			for (int j=0; j<packetSize-1; j++)
				checksum = checksum ^ ((int)buffer[j]& 0xFF);
				     						
			if (checksum_received==checksum){				        
				out_log.write(DataReceivedTime+" ;"+contaT+";"+ax+";"+ay+";"+az+";"+gx+";"+gy+";"+gz+";"+mx+";"+my+";"+mz+";"+checksum_received+";"+checksum/*+";"+test_num+";"+test_state*/+";\n");
				out_log.flush();

				packet_counter_global++;
					
			 	if (packet_counter_global>1000){
			 		//check number packet loss
				 	if ((contaT - contaT_prev)>1)
						packet_loss++;					 
				}
				
			 	contaT_prev=contaT;
			}
			checksum=0;

		
		// Send the obtained bytes to the UI Activity
		float[] echoMsg;
		echoMsg = new float[10];
		echoMsg[0] = ax;
		echoMsg[1] = ay;
		echoMsg[2] = az;
		echoMsg[3] = gx;
		echoMsg[4] = gy;
		echoMsg[5] = gz;                    				
		echoMsg[9] = packet_loss;
		if (DataReceivedTime - lastDataPlotTime > ConfigVals.plotInterval ){
			lastDataPlotTime = DataReceivedTime;
	        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_READ);
	        Bundle bundle = new Bundle();
	        bundle.putFloatArray(MainActivity.SENS_DATA, echoMsg);
	        msg.setData(bundle);
	        mHandler.sendMessage(msg);

		}

	}
	
	
	private void decodeCerebro() throws IOException{
		// ExelSx node, raw data type
		int packetSize = 22;
		int Ch1 = 0,Ch2 = 0,Ch3 = 0,Ch4 = 0,Ch5 = 0,Ch6 = 0,Ch7=0,Ch8=0; //Ch9=0; //channel 9 is dummy can be discarded
		int contaT,checksum = 0,checksum_received,contaT_prev = 0,packet_loss = 0, packet_counter_global = 0;
//		try {
			//read a whole packet:
			while (cnt < packetSize) { 
				buffer[cnt] = (byte) mmInStream.read();
				cnt++;
			}
			contaT = ((int)buffer[2]&0xFF);// (int)(buffer[indiceS + 2]);
			
			Ch1 = (short)((buffer[3]&0xFF)+((buffer[4]&0xFF)*256));
			Ch2 = (short)((buffer[5]&0xFF)+((buffer[6]&0xFF)*256));            						
			Ch3 = (short)((buffer[7]&0xFF)+((buffer[8]&0xFF)*256));

			Ch4 = (short)((buffer[9]&0xFF) +((buffer[10]&0xFF)*256));
			Ch5 = (short)((buffer[11]&0xFF) +((buffer[12]&0xFF)*256));
			Ch6 = (short)((buffer[13]&0xFF) +((buffer[14]&0xFF)*256));
			
			Ch7 = (short)((buffer[15]&0xFF) +((buffer[16]&0xFF)*256));
			Ch8 = (short)((buffer[17]&0xFF) +((buffer[18]&0xFF)*256));
			// Ch9 = (short)((buffer[19]&0xFF) +((buffer[20]&0xFF)*256));

			checksum_received = ((int)buffer[packetSize-1]&0xFF);
			
			//necessary to avoid that newer version of Android (4.3+) closes the connection 
			if (contaT % 100 == 0) 
    			mmOutStream.write('=');
			
			//Verify checksum
			for (int j=0; j<packetSize-1; j++)
				checksum = checksum ^ ((int)buffer[j]& 0xFF);
				     						
			if (checksum_received==checksum){				        
//				out_log.write(DataReceivedTime+" ;"+contaT+";"+Ch1+";"+Ch2+";"+Ch3+";"+Ch4+";"+Ch5+";"+Ch6+";"+Ch7+";"+Ch8+";\n");
//				out_log.flush();

				packet_counter_global++;
					
			 	if (packet_counter_global>1000){
			 		//check number packet loss
				 	if ((contaT - contaT_prev)>1)
						packet_loss++;					 
				}
				
			 	contaT_prev=contaT;
			}
			checksum=0;

		
		// Send the obtained bytes to the UI Activity
		float[] echoMsg;
		echoMsg = new float[10];
		echoMsg[0] = Ch1;
		echoMsg[1] = Ch2;
		echoMsg[2] = Ch3;
		echoMsg[3] = Ch4;
		echoMsg[4] = Ch5;
		echoMsg[5] = Ch6;                    				
		echoMsg[9] = packet_loss;
		if (DataReceivedTime - lastDataPlotTime > ConfigVals.plotInterval ){
			lastDataPlotTime = DataReceivedTime;
	        Message msg = mHandler.obtainMessage(MainActivity.MESSAGE_READ);
	        Bundle bundle = new Bundle();
	        bundle.putFloatArray(MainActivity.SENS_DATA, echoMsg);
	        msg.setData(bundle);
	        mHandler.sendMessage(msg);

		}

	}
	
}
	
