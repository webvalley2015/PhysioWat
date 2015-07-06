package com.niklas.datalogging;

import java.text.DecimalFormat;
import java.util.Arrays;

import com.androidplot.Plot;
import com.androidplot.util.Redrawer;
import com.androidplot.xy.BoundaryMode;
import com.androidplot.xy.LineAndPointFormatter;
import com.androidplot.xy.SimpleXYSeries;
import com.androidplot.xy.XYPlot;
import com.androidplot.xy.XYStepMode;
import com.unibo.cupidnodelogging.R;

import android.app.Activity;
import android.graphics.Color;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

public class UI_Management {
	Activity act;
	BluetoothChatService[] mChatService;
	UI_Management(Activity a, BluetoothChatService[] mChatService){
		this.act =a;
		this.mChatService = mChatService;
	}

    private static final int HISTORY_SIZE = 100;            // number of points to plot in history
    private XYPlot aprHistoryPlot = null;
    private SimpleXYSeries azimuthHistorySeries = null;
    private SimpleXYSeries pitchHistorySeries = null;
    private SimpleXYSeries rollHistorySeries = null;
	
	
	public void checkNodeStatus(BluetoothChatService[] mChatService){
		int state = 0;
		ImageView BTicon = null;
		
		state = mChatService[0].getState();
		BTicon= (ImageView) this.act.findViewById(R.id.imageNode1);
		switch (state){

		case BluetoothChatService.STATE_NONE:
			BTicon.setImageResource(R.drawable.bluetooth_gray);
			break;
		case BluetoothChatService.STATE_DISCONNECTED:
			BTicon.setImageResource(R.drawable.bluetooth_red);
			break;
		case BluetoothChatService.STATE_CONNECTED:
			BTicon.setImageResource(R.drawable.bluetooth_green);
			break;
		case BluetoothChatService.STATE_CONNECTING:
			BTicon.setImageResource(R.drawable.bluetooth_yellow);
			break;
		}
		
		state =mChatService[1].getState();
		BTicon= (ImageView) this.act.findViewById(R.id.imageNode2);
		switch (state){
		case BluetoothChatService.STATE_NONE:
			BTicon.setImageResource(R.drawable.bluetooth_gray);
			break;
		case BluetoothChatService.STATE_DISCONNECTED:
			BTicon.setImageResource(R.drawable.bluetooth_red);
			break;
		case BluetoothChatService.STATE_CONNECTED:
			BTicon.setImageResource(R.drawable.bluetooth_green);
			break;
		case BluetoothChatService.STATE_CONNECTING:
			BTicon.setImageResource(R.drawable.bluetooth_yellow);
			break;
		}
		
		state =mChatService[2].getState();
		BTicon= (ImageView) this.act.findViewById(R.id.imageNode3);
		switch (state){
		case BluetoothChatService.STATE_NONE:
			BTicon.setImageResource(R.drawable.bluetooth_gray);
			break;
		case BluetoothChatService.STATE_DISCONNECTED:
			BTicon.setImageResource(R.drawable.bluetooth_red);
			break;
		case BluetoothChatService.STATE_CONNECTED:
			BTicon.setImageResource(R.drawable.bluetooth_green);
			break;
		case BluetoothChatService.STATE_CONNECTING:
			BTicon.setImageResource(R.drawable.bluetooth_yellow);
			break;
		}

		
		state =mChatService[3].getState();
		BTicon= (ImageView) this.act.findViewById(R.id.imageNode4);
		switch (state){
		case BluetoothChatService.STATE_NONE:
			BTicon.setImageResource(R.drawable.bluetooth_gray);
			break;
		case BluetoothChatService.STATE_DISCONNECTED:
			BTicon.setImageResource(R.drawable.bluetooth_red);
			break;
		case BluetoothChatService.STATE_CONNECTED:
			BTicon.setImageResource(R.drawable.bluetooth_green);
			break;
		case BluetoothChatService.STATE_CONNECTING:
			BTicon.setImageResource(R.drawable.bluetooth_yellow);
			break;
		}
		
		
		state =mChatService[4].getState();
		BTicon= (ImageView) this.act.findViewById(R.id.imageNode5);
		switch (state){
		case BluetoothChatService.STATE_NONE:
			BTicon.setImageResource(R.drawable.bluetooth_gray);
			break;
		case BluetoothChatService.STATE_DISCONNECTED:
			BTicon.setImageResource(R.drawable.bluetooth_red);
			break;
		case BluetoothChatService.STATE_CONNECTED:
			BTicon.setImageResource(R.drawable.bluetooth_green);
			break;
		case BluetoothChatService.STATE_CONNECTING:
			BTicon.setImageResource(R.drawable.bluetooth_yellow);
			break;
		}
		
		
		state =mChatService[5].getState();
		BTicon= (ImageView) this.act.findViewById(R.id.imageNode6);
		switch (state){
		case BluetoothChatService.STATE_NONE:
			BTicon.setImageResource(R.drawable.bluetooth_gray);
			break;
		case BluetoothChatService.STATE_DISCONNECTED:
			BTicon.setImageResource(R.drawable.bluetooth_red);
			break;
		case BluetoothChatService.STATE_CONNECTED:
			BTicon.setImageResource(R.drawable.bluetooth_green);
			break;
		case BluetoothChatService.STATE_CONNECTING:
			BTicon.setImageResource(R.drawable.bluetooth_yellow);
			break;
		}
		
	}
	
	public void checkNames() {

//		for (int i = 0; i< MainActivity.MaxNodes; i++){
//			if (mChatService[i].deviceName != "")
//				ConnectedDevicesNames[i] = mChatService[i].deviceName;
//			else{
//				ConnectedDevicesNames[i] = "Node id";
//			}
//    	}
		TextView NodeText = (TextView) this.act.findViewById(R.id.textNode1);
		NodeText.setText(mChatService[0].deviceName);
		NodeText = (TextView) this.act.findViewById(R.id.textNode2);
		NodeText.setText(mChatService[1].deviceName);
		NodeText = (TextView) this.act.findViewById(R.id.textNode3);
		NodeText.setText(mChatService[2].deviceName);
		NodeText = (TextView) this.act.findViewById(R.id.textNode4);
		NodeText.setText(mChatService[3].deviceName);
		NodeText = (TextView) this.act.findViewById(R.id.textNode5);
		NodeText.setText(mChatService[4].deviceName);		
		NodeText = (TextView) this.act.findViewById(R.id.textNode6);
		NodeText.setText(mChatService[5].deviceName);
	}
	
	public void initBtButtons(){
		
		final ImageView imgView1 = (ImageView) this.act.findViewById(R.id.imageNode1);
		imgView1.setOnClickListener(new View.OnClickListener(){
		    public void onClick(View v) {
		    	nodeToPlot = 0;
		    	checkNodeStatus(mChatService);
		    	imgView1.setImageResource(R.drawable.bluetooth_dark_green);
		    }
		});
		
		final ImageView imgView2 = (ImageView) this.act.findViewById(R.id.imageNode2);
		imgView2.setOnClickListener(new View.OnClickListener(){
		    public void onClick(View v) {
		    	nodeToPlot = 1;
		    	checkNodeStatus(mChatService);
		    	imgView2.setImageResource(R.drawable.bluetooth_dark_green);
		    }
		});
		
		final ImageView imgView3 = (ImageView) this.act.findViewById(R.id.imageNode3);
		imgView3.setOnClickListener(new View.OnClickListener(){
		    public void onClick(View v) {
		    	nodeToPlot = 2;
		    	checkNodeStatus(mChatService);
		    	imgView3.setImageResource(R.drawable.bluetooth_dark_green);
		    }
		});
		final ImageView imgView4 = (ImageView) this.act.findViewById(R.id.imageNode4);
		imgView4.setOnClickListener(new View.OnClickListener(){
		    public void onClick(View v) {
		    	nodeToPlot = 3;
		    	checkNodeStatus(mChatService);
		    	imgView4.setImageResource(R.drawable.bluetooth_dark_green);
		    }
		});
		final ImageView imgView5 = (ImageView) this.act.findViewById(R.id.imageNode5);
		imgView5.setOnClickListener(new View.OnClickListener(){
		    public void onClick(View v) {
		    	nodeToPlot = 4;
		    	checkNodeStatus(mChatService);
		    	imgView5.setImageResource(R.drawable.bluetooth_dark_green);
		    }
		});
		final ImageView imgView6 = (ImageView) this.act.findViewById(R.id.imageNode6);
		imgView6.setOnClickListener(new View.OnClickListener(){
		    public void onClick(View v) {
		    	nodeToPlot = 5;
		    	checkNodeStatus(mChatService);
		    	imgView6.setImageResource(R.drawable.bluetooth_dark_green);
		    }
		});
	}

	
	private int nodeToPlot = 0;
	
	public void checkDataRead(int nodeData, float[] data) {
		
		if(nodeData == nodeToPlot){
			if (rollHistorySeries.size() > HISTORY_SIZE) {
		        rollHistorySeries.removeFirst();
		        pitchHistorySeries.removeFirst();
		        azimuthHistorySeries.removeFirst();
		    }
		 
		    // add the latest history sample:
			azimuthHistorySeries.addLast(null, data[0]);
			pitchHistorySeries.addLast(null, data[1]);
			rollHistorySeries.addLast(null, data[2]);
		}
	}
	
	public void deInitGraph(){
		aprHistoryPlot.clear();
		aprHistoryPlot = null;
		azimuthHistorySeries = null;
		pitchHistorySeries = null;
		rollHistorySeries = null;
	}
	
	public Redrawer initGraph(){
		aprHistoryPlot = (XYPlot) this.act.findViewById(R.id.aprHistoryPlot);

        azimuthHistorySeries = new SimpleXYSeries("Acc X");
        azimuthHistorySeries.useImplicitXVals();
        pitchHistorySeries = new SimpleXYSeries("Acc Y");
        pitchHistorySeries.useImplicitXVals();
        rollHistorySeries = new SimpleXYSeries("Acc Z");
        rollHistorySeries.useImplicitXVals();

        aprHistoryPlot.setRangeBoundaries(-32000, 32000, BoundaryMode.FIXED);
        aprHistoryPlot.setDomainBoundaries(0, HISTORY_SIZE, BoundaryMode.FIXED);
        aprHistoryPlot.addSeries(azimuthHistorySeries,
                new LineAndPointFormatter(
                        Color.rgb(100, 100, 200), null, null, null));
        aprHistoryPlot.addSeries(pitchHistorySeries,
                new LineAndPointFormatter(
                        Color.rgb(100, 200, 100), null, null, null));
        aprHistoryPlot.addSeries(rollHistorySeries,
                new LineAndPointFormatter(
                        Color.rgb(200, 100, 100), null, null, null));
        aprHistoryPlot.setDomainStepMode(XYStepMode.INCREMENT_BY_VAL);
        aprHistoryPlot.setDomainStepValue(HISTORY_SIZE/10);
        aprHistoryPlot.setTicksPerRangeLabel(3);
        aprHistoryPlot.setDomainLabel("Sample Index");
        aprHistoryPlot.getDomainLabelWidget().pack();
        aprHistoryPlot.setRangeLabel("Angle (Degs)");
        aprHistoryPlot.getRangeLabelWidget().pack();

        aprHistoryPlot.setRangeValueFormat(new DecimalFormat("#"));
        aprHistoryPlot.setDomainValueFormat(new DecimalFormat("#"));
        
        Redrawer redrawer = new Redrawer(
                Arrays.asList(new Plot[]{aprHistoryPlot}),
                20, false);
        return redrawer;
	}
	
}
