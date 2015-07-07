
$(document).ready(function()  {

var usr_form_input = document.getElementById("id_username");

    if (usr_form_input !== null) {
        usr_form_input.setAttribute("placeholder","Username*");
	usr_form_input.setAttribute("width","100%");
	}

});


$(document).ready(function()  {

var pass_form_input = document.getElementById("id_password");

    if (pass_form_input !== null) {
        pass_form_input.setAttribute("placeholder","Password*");
    }


});




$(document).ready(function()  {

var pass_form_input = document.getElementById("id_device");

    if (pass_form_input !== null) {
        pass_form_input.setAttribute("style","display:none");
    }


});


$(document).ready(function()  {

var pass_form_input = document.getElementById("id_description");

    if (pass_form_input !== null) {
        pass_form_input.setAttribute("style","display:none");
    }


});




$(document).ready(function()  {

var pass_form_input = document.getElementById("id_password");

    if (pass_form_input !== null) {
        pass_form_input.setAttribute("style","display:none");
    }


});



$(document).ready(function()  {

var pass_form_input = document.getElementById("BuSu");

    if (pass_form_input !== null) {
        pass_form_input.setAttribute("style","display:none");
    }


});


$(document).ready(function()  {

var pass_form_input = document.getElementById("BuRe");

    if (pass_form_input !== null) {
        pass_form_input.setAttribute("style","display:none");
    }


});





/*
$(document).ready(function()  {

var usr_form_input = document.getElementById("id_username");

    if (usr_form_input !== null) {
        usr_form_input.setAttribute("placeholder","Username*");
	usr_form_input.setAttribute("width","100%");
	}

});
*/

//var col.style.backgroundcolor

function show_hide_upload(passage){
	if (passage==0) {
		document.getElementById("sel").style.display = 'block';
		document.getElementById("id_file").style.display = 'block';
		document.getElementById("Experiment_div").style.display = 'block';
		document.getElementById("div_step_1").setAttribute("style","background-color:#6699FF; color:white; border-right:2px solid #6699FF; height:100%; text-align: center; padding-top:3.8%");
	} else {
		document.getElementById("id_file").style.display = 'none';
		document.getElementById("sel").style.display = 'none';
		document.getElementById("Experiment_div").style.display = 'none';
		document.getElementById("div_step_1").setAttribute("style","background-color:#F6F6F6; color:black; border-right:2px solid #6699FF; height:100%; text-align: center; padding-top:3.8%");
	}
	if (passage==1) {
		document.getElementById("id_description").style.display = 'block';
		document.getElementById("id_device").style.display = 'block';
		document.getElementById("div_step_2").setAttribute("style","background-color:#6699FF; color:white; border-right:2px solid #6699FF; height:100%; text-align: center; padding-top:3.8%");
	} else {
		document.getElementById("id_description").style.display = 'none';
		document.getElementById("id_device").style.display = 'none';
		document.getElementById("div_step_2").setAttribute("style","background-color:#F6F6F6; color:black; border-right:2px solid #6699FF; height:100%; text-align: center; padding-top:3.8%");
	}
	if (passage==2) {
		document.getElementById("id_password").style.display = 'block';
		//document.getElementById("BuSu").style.display = 'block';
		//document.getElementById("BuRe").style.display = 'block';
		document.getElementById("div_step_3").setAttribute("style","background-color:#6699FF; color:white; border-right:2px solid #6699FF; height:100%; text-align: center; padding-top:3.8%");
	} else {
		document.getElementById("id_password").style.display = 'none';
		//document.getElementById("BuSu").style.display = 'none';
		//document.getElementById("BuRe").style.display = 'none';
		document.getElementById("div_step_3").setAttribute("style","background-color:#F6F6F6; color:black; border-right:2px solid #6699FF; height:100%; text-align: center; padding-top:3.8%");
	}
}

passage=0

function decrease_passage()
{
	if(passage>0){
		passage -=1
		show_hide_upload(passage)
	}
}


function increase_passage()
{
	if(passage<2){
		passage +=1
		show_hide_upload(passage)
	}
}


