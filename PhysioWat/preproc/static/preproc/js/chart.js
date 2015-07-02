console.log("file javascript loaded");
/** 
 * this function is up to call the function get data of the class
 *  lineg raph of the views, which is, read the json e return data
 */
 

///PICK DATA
function ajax_get_data( where="chartbox" ) {
	var url = '/preproc/linegraph_getdata/';
	
	// $ == jQuery, è la stessa variabile !!!!!!
	$.ajax(url,    
		   {cache: false,
			///async: false,
			dataType: "json",
			error: function () {
						console.log("errore prendendo i dati!!");
				   },
			method: "GET",
			success: function (data_received) {
						create_graph(data_received, where);
				   },  
		   }
	);  
}


function create_graph(data, where)
{
	if (data['chart'] == undefined) {
		data['chart'] = {};	
	}
	
	data['chart']['renderTo'] = where;
	
	
	var chart = new Highcharts.Chart(data);
	
}
