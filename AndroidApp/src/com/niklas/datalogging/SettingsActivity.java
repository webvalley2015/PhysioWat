package com.niklas.datalogging;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import com.unibo.cupidnodelogging.R;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewStub;
import android.view.Window;
import android.view.ViewStub.OnInflateListener;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.Toast;

public class SettingsActivity extends Activity{

	private List<String> ConnectedNodes = new ArrayList<String>();
	private ArrayList<String> confVals = new ArrayList<String>();
	
	protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_INDETERMINATE_PROGRESS);
        setContentView(R.layout.settings_layout);
        ConnectedNodes.add("Cupid Node");
        ConnectedNodes.add("Generic Node");
    }

	protected void onStart() {
        super.onStart();
        initSpinners();
//        ConnectedNodes.add(getIntent().getExtras().getString(MainActivity.keyBundle));
//        fillSpinner((Spinner) findViewById(R.id.spinnerNodeList) , ConnectedNodes);
        Button button= (Button) findViewById(R.id.buttonSubmit);
        
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
            	if (ConfigVals.nodeType == ConfigVals.EXELs1_NODE ||
            			ConfigVals.nodeType == ConfigVals.EXELs3_NODE){
	//            	byte res[] = GetFSconfValues();
	            	confVals.add(0,GetFSconfValues());
	            	confVals.add(1,GetSamplingFreqConfString());
	            	confVals.add(2,GetDataTypeConfString());
	            	String start = "= =";
	            	String stop = ": :";
	            	ConfigVals.startStr = start.toCharArray(); 
	            	ConfigVals.stopStr = stop.toCharArray();
	            	
	            	

            	}
            	else if (ConfigVals.nodeType == ConfigVals.GENERIC_NODE){
            		EditText startCmd = (EditText) findViewById(R.id.editTextSartCmd);
            		ConfigVals.startStr = startCmd.getText().toString().toCharArray();
            		EditText stopCmd = (EditText) findViewById(R.id.editTextStopCmd);
            		ConfigVals.stopStr = stopCmd.getText().toString().toCharArray();
            		String customConfig = ((EditText) findViewById(R.id.editTextCustomStr)).getText().toString();
            		confVals.add(customConfig);
            		
            	}
            	else if (ConfigVals.nodeType == ConfigVals.FLORIMAGE_NODE){
	            	String start = "s";
	            	String stop = "e";
	            	ConfigVals.startStr = start.toCharArray(); 
	            	ConfigVals.stopStr = stop.toCharArray();
            	}
            	else if (ConfigVals.nodeType == ConfigVals.CEREBRO_NODE){
	            	String start = "= =";
	            	String stop = ": :";
	            	ConfigVals.startStr = start.toCharArray(); 
	            	ConfigVals.stopStr = stop.toCharArray();
            	}
            	
            	Intent returnIntent = new Intent();
            	Bundle mBundle = new Bundle();
            	mBundle.putStringArrayList("result", confVals);
            	returnIntent.putStringArrayListExtra("result", confVals);
            	setResult(RESULT_OK,returnIntent);
               finish();
            }
        });	
       
        
	}
	


	    public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
	        String selected = parent.getItemAtPosition(pos).toString();
	    }

	    public void onNothingSelected(AdapterView parent) {
	        // Do nothing.
	    }


	private String GetFSconfValues(){
		byte[] confSeq = new byte[7+1];
		byte CommandIndex = 0;
        char checksum = 0;
    	Spinner AccFS = (Spinner) findViewById(R.id.spinnerAccFullScale);
    	Spinner GyrFS = (Spinner) findViewById(R.id.spinnerGyrFullScale);
		confSeq[CommandIndex++]  = 100;  //Command
		confSeq[CommandIndex++]  = 0;    //Number of Bytes	
		confSeq[CommandIndex++]  = 52;	 // Start Addr
		confSeq[CommandIndex++]  = 0;
		confSeq[CommandIndex++]  = (byte) AccFS.getSelectedItemPosition();
		confSeq[CommandIndex++]  = (byte) GyrFS.getSelectedItemPosition();
		
		confSeq[1] = (byte) (CommandIndex-4); 
		
        for (int i = 0; i < CommandIndex; i++)
        {
            checksum += confSeq[i];
        }
        confSeq[CommandIndex++] = (byte) checksum;
        confSeq[CommandIndex] = 0x00;
        String str = new String(confSeq);
		
		return str;
	}
	
	private String GetSamplingFreqConfString(){
		byte[] confSeq = new byte[6];
        byte CommandIndex = 0;
        byte checksum = 0;
        Spinner SamplRate = (Spinner) findViewById(R.id.spinnerSampleRate);
		confSeq[CommandIndex++]  = 100;  //Command
		confSeq[CommandIndex++]  = 0;    //Number of Bytes	
		confSeq[CommandIndex++]  = 80;	 // Start Addr
		confSeq[CommandIndex++]  = 0;
		confSeq[CommandIndex++]  = (byte) SamplRate.getSelectedItemPosition();

		confSeq[1] = (byte) (CommandIndex-4); 
		
        for (int i = 0; i < CommandIndex; i++)
        {
            checksum += confSeq[i];
        }
        confSeq[CommandIndex] = checksum;

        String str = new String(confSeq);
		
		return str;
	}
	
	
	private String GetDataTypeConfString(){
		byte[] confSeq = new byte[6];
        byte CommandIndex = 0;
        byte checksum = 0;
        Spinner SamplRate = (Spinner) findViewById(R.id.spinnerDataType);
		confSeq[CommandIndex++]  = 100;  //Command
		confSeq[CommandIndex++]  = 0;    //Number of Bytes	
		confSeq[CommandIndex++]  = 56;	 // Start Addr
		confSeq[CommandIndex++]  = 0;
		confSeq[CommandIndex++]  = (byte) SamplRate.getSelectedItemPosition();

		confSeq[1] = (byte) (CommandIndex-4); 
		
        for (int i = 0; i < CommandIndex; i++)
        {
            checksum += confSeq[i];
        }
        confSeq[CommandIndex] = checksum;

        String str = new String(confSeq);
		
		return str;
	}
	
	
	
	
	private void initSpinners(){
		
		
		 	List<String> SamplingRates =  new ArrayList<String>();
	        SamplingRates.add("200 Hz");
	        SamplingRates.add("100 Hz");
	        SamplingRates.add("50 Hz");
	        SamplingRates.add("32 Hz");
	        SamplingRates.add("16 Hz");
	        Spinner samplingSpinner = (Spinner)findViewById(R.id.spinnerSampleRate);
	        fillSpinner(samplingSpinner  , SamplingRates);
	        samplingSpinner.setOnItemSelectedListener(
	        		new OnItemSelectedListener() {
	        			public void onItemSelected(
	                            AdapterView<?> parent, View view, int position, long id) {
	                        showToast("Spinner1: position=" + position + " id=" + id);
	                    }

	                    public void onNothingSelected(AdapterView<?> parent) {
	                        showToast("Spinner1: unselected");
	                    }
	        		});
	        
	        List<String> NodeType =  new ArrayList<String>();
	        for (String node : ConfigVals.nodeTypeName){
	        	NodeType.add(node);
	        }
	        Spinner nodeTypeSpinner = (Spinner)findViewById(R.id.spinnerNodeType);
	        fillSpinner(nodeTypeSpinner  , NodeType);
	        nodeTypeSpinner.setOnItemSelectedListener(
	        		new OnItemSelectedListener() {
	        			public void onItemSelected(
	                            AdapterView<?> parent, View view, int position, long id) {
	        					ConfigVals.nodeType = position;
	    	                    SetGraphicsNodeType();
//	                        showToast("Spinner1: position=" + position + " id=" + id);
	                    }
	                    public void onNothingSelected(AdapterView<?> parent) {
//	                        showToast("Spinner1: unselected");
	                    }
	        		});
	        
	        List<String> AccFS =  new ArrayList<String>();
	        AccFS.add("2 g");
	        AccFS.add("4 g");
	        AccFS.add("8 g");
	        AccFS.add("16 g");
	        fillSpinner((Spinner) findViewById(R.id.spinnerAccFullScale) , AccFS);
	        
	        List<String> GyrFS =  new ArrayList<String>();
	        GyrFS.add("250 dps");
	        GyrFS.add("500 dps");
	        GyrFS.add("1000 dps");
	        GyrFS.add("2000 dps");
	        fillSpinner((Spinner) findViewById(R.id.spinnerGyrFullScale) , GyrFS);
	        
	        List<String> DatType =  new ArrayList<String>();
	        DatType.add("Raw");
	        DatType.add("Calibrated");
	        DatType.add("Quaternions");
	        DatType.add("Quat + calib");
	        fillSpinner((Spinner) findViewById(R.id.spinnerDataType) , DatType);
	        

	}
	private void fillSpinner(Spinner spinnerId, List<String> data){
		
		ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, data);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        Spinner sItems = (Spinner) spinnerId;
        sItems.setAdapter(adapter);
	}
	
	private void SetGraphicsNodeType(){
		TableLayout layout = null;
		switch (ConfigVals.nodeType){
		case ConfigVals.GENERIC_NODE:
			layout = (TableLayout) findViewById(R.id.layoutCupidNode);
			for (int i = 0; i < layout.getChildCount(); i++) {
			    TableRow child = (TableRow) layout.getChildAt(i);
			    for (int j = 0; j< child.getChildCount(); j++){
			    	View subchild = child.getChildAt(j);
			    	subchild.setEnabled(false);
			    }
			    child.setEnabled(false);
//			    child.setVisibility(View.VISIBLE);
			}
			layout = (TableLayout) findViewById(R.id.layoutGenericNode);
			for (int i = 0; i < layout.getChildCount(); i++) {
				 TableRow child = (TableRow) layout.getChildAt(i);
				    for (int j = 0; j< child.getChildCount(); j++){
				    	View subchild = child.getChildAt(j);
				    	subchild.setEnabled(true);
				    }
				    child.setEnabled(true);
//			    child.setVisibility(View.INVISIBLE);
			}
			break;
		case ConfigVals.CEREBRO_NODE:
			layout = (TableLayout) findViewById(R.id.layoutCupidNode);
			for (int i = 0; i < layout.getChildCount(); i++) {
			    TableRow child = (TableRow) layout.getChildAt(i);
			    for (int j = 0; j< child.getChildCount(); j++){
			    	View subchild = child.getChildAt(j);
			    	subchild.setEnabled(false);
			    }
			    child.setEnabled(false);
//			    child.setVisibility(View.VISIBLE);
			}
			layout = (TableLayout) findViewById(R.id.layoutGenericNode);
			for (int i = 0; i < layout.getChildCount(); i++) {
				 TableRow child = (TableRow) layout.getChildAt(i);
				    for (int j = 0; j< child.getChildCount(); j++){
				    	View subchild = child.getChildAt(j);
				    	subchild.setEnabled(false);
				    }
				    child.setEnabled(false);
//			    child.setVisibility(View.INVISIBLE);
			}
			break;
		case ConfigVals.EXELs1_NODE:
		case ConfigVals.EXELs3_NODE:
			layout = (TableLayout) findViewById(R.id.layoutCupidNode);
			for (int i = 0; i < layout.getChildCount(); i++) {
			    TableRow child = (TableRow) layout.getChildAt(i);
			    for (int j = 0; j< child.getChildCount(); j++){
			    	View subchild = child.getChildAt(j);
			    	subchild.setEnabled(true);
			    }
			    child.setEnabled(true);
//			    child.setVisibility(View.VISIBLE);
			}
			layout = (TableLayout) findViewById(R.id.layoutGenericNode);
			for (int i = 0; i < layout.getChildCount(); i++) {
				 TableRow child = (TableRow) layout.getChildAt(i);
				    for (int j = 0; j< child.getChildCount(); j++){
				    	View subchild = child.getChildAt(j);
				    	subchild.setEnabled(false);
				    }
				    child.setEnabled(false);
//			    child.setVisibility(View.INVISIBLE);
			}

			break;
		}
	}
	
	
    protected void onPause() {
        super.onPause();
       
    }
    
    void showToast(CharSequence msg) {
        Toast.makeText(this, msg, Toast.LENGTH_SHORT).show();
    }
	
	
}
