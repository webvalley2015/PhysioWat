console.log("file javascript loaded");
/** 
 * this function is up to call the function get data of the class
 *  lineg raph of the views, which is, read the json e return data
 */
 
 var data = {};
///PICK DATA
function ajax_get_data() {
	var url = '/preproc/linegraph_getdata/'
	
	// $ == jQuery, è la stessa variabile !!!!!!
	$.ajax(url,    
		   {cache: false,
			async: false,
			dataType: "json",
			error: function () {
						console.log("errore prendendo i dati!!");
				   },
			method: "GET",
			success: function (data_recieved) {
						console.log("got the data!!");
						create_graph(data_recieved);
				   },  
		   }
	);  
}


function create_graph(data)
{
	if (data['chart'] == undefined)
	{
		data['chart'] = {};	
	}
	
	data['chart']['renderTo'] = "chartbox";
	
	
	var chart = new Highcharts.Chart(data);
	
}

$(document).ready(function() {
	ajax_get_data();
	}
);
